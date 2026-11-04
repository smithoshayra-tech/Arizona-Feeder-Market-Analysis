"""Independent checks. Recomputes the key figures from the raw CSVs with pandas only
(no SQL) and compares them with the SQL-driven outputs. Writes outputs/validation_report.md."""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs"
checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))


ip = pd.read_csv(RAW / "ipeds_first_time_freshmen_by_residence.csv")
wi = pd.read_csv(RAW / "wiche_hs_graduates_by_state.csv")
sref = pd.read_csv(RAW / "state_reference.csv")
inst = {104179: "UA", 104151: "ASU", 105330: "NAU"}
ip["inst"] = ip.unitid.map(inst)

# --- Source integrity ---------------------------------------------------------
for (u, y), d in ip.groupby(["unitid", "year"]):
    r = d.set_index("residence_code").first_time_freshmen
    states = r[(r.index >= 1) & (r.index <= 56)].sum()
    check(f"IPEDS {inst[u]} {y}: states + DC + 'unknown state' = U.S. total (row 58)",
          states + r.get(57, 0) == r[58], f"{states}+{r.get(57,0)} vs {r[58]}")
    check(f"IPEDS {inst[u]} {y}: U.S. total + outlying areas + foreign = grand total (row 99)",
          r[58] + r.get(89, 0) + r.get(90, 0) == r[99], f"{r[58]}+{r.get(89,0)}+{r.get(90,0)} vs {r[99]}")
check("WICHE: 51 jurisdictions x 33 class years, no duplicates",
      len(wi) == 51 * 33 and not wi.duplicated(["state", "class_year"]).any(), f"{len(wi)} rows")

# --- Independent recomputation ------------------------------------------------
st = ip.merge(sref, left_on="residence_code", right_on="fips")
pen = st.merge(wi, left_on=["state", "year"], right_on=["state", "class_year"])
pen["per_1000"] = 1000 * pen.first_time_freshmen / pen.hs_graduates

mk = pd.read_csv(OUT / "market_ranking.csv").set_index("state")
ua24 = st[(st.inst == "UA") & (st.year == 2024)].set_index("state").first_time_freshmen
g = wi.pivot(index="state", columns="class_year", values="hs_graduates")
ok_counts = all(int(mk.loc[s, "ua_2024"]) == int(ua24.get(s, 0)) for s in mk.index)
check("Market table: UA 2024 freshmen per state match the raw file (50 markets)", ok_counts)
ok_out = np.allclose([mk.loc[s, "outlook_2030"] for s in mk.index], [g.loc[s, 2030] / g.loc[s, 2024] - 1 for s in mk.index])
check("Market table: projected change 2024 to 2030 matches the raw WICHE file", ok_out)
ok_pen = np.allclose([mk.loc[s, "ua_per_1000"] for s in mk.index],
                     [1000 * ua24.get(s, 0) / g.loc[s, 2024] for s in mk.index])
check("Market table: UA freshmen per 1,000 graduates matches independent calculation", ok_pen)

# Rank recomputation
pct = lambda s: s.rank(pct=True)
avg = g.loc[mk.index, list(range(2025, 2031))].mean(axis=1)
sc = 100 * (0.4 * pct(avg) + 0.3 * pct(mk.outlook_2030) + 0.3 * pct(mk.ua_per_1000))
check("Priority score: independent recomputation equals stored score", np.allclose(sc, mk.priority_score))

# Scenario arithmetic: hold-2024-rate, 2030
r24 = pen[(pen.inst == "UA") & (pen.year == 2024)].set_index("state").per_1000
r24 = r24.reindex(g.index).fillna(0)
hold2030 = (r24.drop("AZ") * g.drop("AZ")[2030] / 1000).sum()
sc_df = pd.read_csv(OUT / "scenarios_2025_2030.csv")
stored = sc_df[(sc_df.scenario == "hold_2024_state_rates") & (sc_df.class_year == 2030)].out_of_state.iloc[0]
check("Scenario hold-2024-rates, 2030 out-of-state: independent value equals stored", abs(hold2030 - stored) < 1e-6,
      f"{hold2030:.1f}")
base24 = ua24.drop("AZ", errors="ignore").sum()
check("2024 out-of-state baseline (49 states + DC) = sum of state rows", base24 == 3823, str(base24))

# --- Facts quoted in the README and chart titles -------------------------------
mix = pd.read_csv(OUT / "residency_mix.csv")
f = {}
for i in ("UA", "ASU", "NAU"):
    f[f"out_of_state_share_2024_{i}"] = round(100 * mix[(mix.inst == i) & (mix.year == 2024)].out_of_state_share.iloc[0], 1)
f["ua_out_of_state_share_2018_2022_2024"] = [round(100 * x, 1) for x in mix[mix.inst == "UA"].out_of_state_share]
f["ca_share_of_ua_out_of_state_2024"] = round(100 * mk.loc["CA", "ua_2024"] / base24, 1)
f["ca_outlook_2030_pct"] = round(100 * mk.loc["CA", "outlook_2030"], 1)
f["il_outlook_2030_pct"] = round(100 * mk.loc["IL", "outlook_2030"], 1)
oos_g = lambda y: g.drop("AZ")[y].sum()
f["out_of_state_grads_change_2024_2030_pct"] = round(100 * (oos_g(2030) / oos_g(2024) - 1), 2)
f["az_grads_2024_2030_2034_2041"] = [int(g.loc["AZ", y]) for y in (2024, 2030, 2034, 2041)]
f["hold_rate_2030_out_of_state"] = round(stored)
f["hold_vs_2024_pct"] = round(100 * (stored / base24 - 1), 1)
f["hold_vs_2024_delta"] = round(stored - base24)
w5 = sc_df[(sc_df.scenario == "whatif_top5_plus10pct") & (sc_df.class_year == 2030)].out_of_state.iloc[0]
f["whatif_2030"] = round(w5); f["whatif_gain_vs_hold_2030"] = round(w5 - stored)
lo = sc_df[(sc_df.scenario == "low_observed_pooled_rate") & (sc_df.class_year == 2030)].out_of_state.iloc[0]
hi = sc_df[(sc_df.scenario == "high_observed_pooled_rate") & (sc_df.class_year == 2030)].out_of_state.iloc[0]
f["low_high_2030"] = [round(lo), round(hi)]
rates = pd.read_csv(OUT / "ua_out_of_state_rate_by_year.csv").set_index("year").per_1000
f["pooled_rates_2018_2022_2024"] = [round(x, 3) for x in rates]
top10 = mk.sort_values("grads_avg_2025_2030", ascending=False).head(10)
f["top10_pools"] = list(top10.index)
f["asu_above_ua_in_top10"] = int((top10.asu_per_1000 > top10.ua_per_1000).sum())
f["asu_equal_ua_in_top10"] = list(top10.index[top10.asu_per_1000 == top10.ua_per_1000])
f["top5_score"] = list(mk.sort_values("priority_score", ascending=False).head(5).index)
f["tiers"] = {t: list(d.index) for t, d in mk.groupby("tier")}
f["sensitivity"] = pd.read_csv(OUT / "ranking_sensitivity.csv", index_col=0).round(2).to_dict("index")
f["thin_markets"] = list(mk[mk.thin_evidence].index)
f["ua_top3_2024"] = {s: int(mk.loc[s, "ua_2024"]) for s in mk.sort_values("ua_2024", ascending=False).head(3).index}

lines = ["# Validation report", "", f"{sum(c[1] for c in checks)} of {len(checks)} checks passed.", "",
         "| Check | Result | Detail |", "|---|---|---|"]
lines += [f"| {n} | {'PASS' if ok else 'FAIL'} | {d} |" for n, ok, d in checks]
lines += ["", "## Figures quoted in the README and chart titles", "", "```"]
import json
lines += [json.dumps(f, indent=1, default=str), "```"]
(OUT / "validation_report.md").write_text("\n".join(lines))
print(f"{sum(c[1] for c in checks)} of {len(checks)} checks passed")
for n, ok, d in checks:
    if not ok:
        print("FAIL:", n, d)
print(json.dumps(f, indent=1, default=str))
