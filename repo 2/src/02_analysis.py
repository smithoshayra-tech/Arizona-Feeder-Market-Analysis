"""Rank out-of-state feeder markets for the University of Arizona and run enrollment scenarios.

Inputs : data/processed/feeder.db (built by 01_build_database.py)
Outputs: outputs/*.csv
"""
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
con = sqlite3.connect(ROOT / "data" / "processed" / "feeder.db")

# Scoring weights are an assumption, not a finding. Sensitivity runs below test them.
WEIGHTS = {"pool": 0.4, "outlook": 0.3, "traction": 0.3}
ALT_WEIGHTS = {
    "equal": {"pool": 1 / 3, "outlook": 1 / 3, "traction": 1 / 3},
    "pool_heavy": {"pool": 0.6, "outlook": 0.2, "traction": 0.2},
    "outlook_heavy": {"pool": 0.2, "outlook": 0.6, "traction": 0.2},
    "traction_heavy": {"pool": 0.2, "outlook": 0.2, "traction": 0.6},
}
THIN = 10  # fewer than this many UA freshmen in 2024 = thin evidence


def q(sql, **kw):
    return pd.read_sql_query(sql, con, **kw)


# 1. Residency mix -----------------------------------------------------------
mix = q("SELECT * FROM v_residency_mix ORDER BY inst, year")
mix["in_state_share"] = mix.arizona / mix.total_freshmen
mix["out_of_state_us"] = mix.us_total - mix.arizona
mix["out_of_state_share"] = mix.out_of_state_us / mix.total_freshmen
mix["foreign_share"] = mix.foreign_residents / mix.total_freshmen
mix.to_csv(OUT / "residency_mix.csv", index=False)

# 2. Market table ------------------------------------------------------------
m = q("SELECT * FROM v_market_base")
# IPEDS lists only states that sent at least one student; a missing row means zero.
for c in ["ua_2018", "ua_2022", "ua_2024", "asu_2024", "nau_2024"]:
    m[c] = m[c].fillna(0).astype(int)
for inst in ("ua", "asu", "nau"):
    m[f"{inst}_per_1000"] = 1000 * m[f"{inst}_2024"] / m["grads_2024"]
m["ua_change_2018_2024"] = m.ua_2024 - m.ua_2018
m["outlook_2030"] = m.grads_2030 / m.grads_2024 - 1
m["outlook_2035"] = m.grads_2035 / m.grads_2024 - 1


def score(df, w):
    pct = lambda s: s.rank(pct=True)
    return (w["pool"] * pct(df.grads_avg_2025_2030)
            + w["outlook"] * pct(df.outlook_2030)
            + w["traction"] * pct(df.ua_per_1000)) * 100


m["priority_score"] = score(m, WEIGHTS)
m["rank"] = m.priority_score.rank(ascending=False, method="min").astype(int)
m["thin_evidence"] = m.ua_2024 < THIN
m = m.sort_values("rank")
m.to_csv(OUT / "market_ranking.csv", index=False)

# 3. Sensitivity of the ranking to the weights --------------------------------
sens = {}
for name, w in ALT_WEIGHTS.items():
    r = score(m, w).rank(ascending=False, method="min")
    top10 = set(m.loc[r <= 10, "state"])
    sens[name] = {
        "spearman_vs_base": float(pd.Series(r.values).corr(pd.Series(m["rank"].values), method="spearman")),
        "top10_overlap_with_base": len(top10 & set(m.loc[m["rank"] <= 10, "state"])),
    }
sens = pd.DataFrame(sens).T
sens.to_csv(OUT / "ranking_sensitivity.csv")

# 4. Peer benchmark in the largest pools --------------------------------------
peer = m.sort_values("grads_avg_2025_2030", ascending=False).head(15)[
    ["state", "state_name", "grads_2024", "ua_2024", "asu_2024", "nau_2024",
     "ua_per_1000", "asu_per_1000", "nau_per_1000"]].copy()
peer["asu_to_ua_ratio"] = peer.asu_per_1000 / peer.ua_per_1000
peer.to_csv(OUT / "peer_benchmark_top15_pools.csv", index=False)

# 5. Arizona home-market pool and penetration ---------------------------------
az = q("""SELECT p.inst, p.year, p.freshmen, p.hs_graduates, p.per_1000_grads
          FROM v_penetration p WHERE p.state='AZ' ORDER BY p.inst, p.year""")
az.to_csv(OUT / "arizona_home_market.csv", index=False)
az_pool = q("SELECT class_year, hs_graduates, data_status FROM wiche_hs_grads WHERE state='AZ' ORDER BY class_year")
az_pool.to_csv(OUT / "arizona_hs_graduates.csv", index=False)

# 6. Scenarios, class years 2025-2030 -----------------------------------------
# Out-of-state (49 states + DC) freshmen per 1,000 graduates is the planning rate.
# The low and high cases are the lowest and highest rates actually observed in 2018, 2022 and 2024.
pen = q("SELECT inst, year, state, freshmen, hs_graduates, per_1000_grads FROM v_penetration WHERE inst='UA'")
oos = pen[pen.state != "AZ"].groupby("year")[["freshmen", "hs_graduates"]].sum()
oos["per_1000"] = 1000 * oos.freshmen / oos.hs_graduates
oos.to_csv(OUT / "ua_out_of_state_rate_by_year.csv")

grads = q("SELECT state, class_year, hs_graduates FROM wiche_hs_grads WHERE class_year BETWEEN 2024 AND 2030")
G = grads.pivot(index="state", columns="class_year", values="hs_graduates")
years = list(range(2025, 2031))
az_rate = pen[(pen.state == "AZ") & (pen.year == 2024)].per_1000_grads.iloc[0]
pen24 = pen[pen.year == 2024].set_index("state").per_1000_grads.reindex(G.index).fillna(0.0)
top5 = list(m.head(5).state)
UPLIFT = 0.10  # what-if only: relative lift in penetration in the top 5 markets


def scenario(name, oos_rate=None, uplift_states=()):
    rows = []
    for y in years:
        az_n = az_rate * G.loc["AZ", y] / 1000
        if oos_rate is None:  # state-by-state 2024 rates
            r = pen24.copy()
            for st in uplift_states:
                r[st] = r[st] * (1 + UPLIFT)
            oos_n = (r.drop("AZ") * G.drop("AZ")[y] / 1000).sum()
        else:                 # one pooled rate applied to all out-of-state graduates
            oos_n = oos_rate * G.drop("AZ")[y].sum() / 1000
        rows.append({"scenario": name, "class_year": y, "arizona": az_n,
                     "out_of_state": oos_n, "total": az_n + oos_n})
    return pd.DataFrame(rows)


scen_df = pd.concat([
    scenario("hold_2024_state_rates"),
    scenario("low_observed_pooled_rate", oos.per_1000.min()),
    scenario("high_observed_pooled_rate", oos.per_1000.max()),
    scenario("whatif_top5_plus10pct", None, top5),
])
scen_df.to_csv(OUT / "scenarios_2025_2030.csv", index=False)

# 7. Market tiers --------------------------------------------------------------
agg24 = oos.loc[2024, "per_1000"]
big = m.grads_avg_2025_2030.quantile(0.75)
def tier(r):
    large, strong = r.grads_avg_2025_2030 >= big, r.ua_per_1000 >= agg24
    return {(True, True): "Core: large pool, strong traction",
            (True, False): "Build: large pool, below-average traction",
            (False, True): "Niche: smaller pool, strong traction",
            (False, False): "Monitor"}[(large, strong)]
m["tier"] = m.apply(tier, axis=1)
m.to_csv(OUT / "market_ranking.csv", index=False)
print("\nPooled out-of-state rate per 1,000 grads:\n", oos.round(3), "\nlarge-pool threshold:", round(big), "agg24:", round(agg24, 3))
print(m.groupby("tier").state.apply(list))

# 2024 reference: US state + DC freshmen (excludes unknown state, territories, foreign)
ref2024 = q("""SELECT SUM(freshmen) AS freshmen FROM v_state_freshmen WHERE inst='UA' AND year=2024""").freshmen[0]
print("UA 2024 freshmen from 50 states+DC:", ref2024)
print("\nResidency mix:\n", mix.round(3).to_string(index=False))
cols = ["rank", "state", "ua_2018", "ua_2024", "grads_2024", "grads_avg_2025_2030", "outlook_2030",
        "ua_per_1000", "asu_per_1000", "priority_score", "thin_evidence"]
print("\nTop 15 markets:\n", m[cols].head(15).round(3).to_string(index=False))
print("\nBottom 5:\n", m[cols].tail(5).round(3).to_string(index=False))
print("\nSensitivity:\n", sens.round(3))
print("\nPeer benchmark:\n", peer.round(2).to_string(index=False))
print("\nScenarios:\n", scen_df.round(0).to_string(index=False))
print("top5:", top5)
