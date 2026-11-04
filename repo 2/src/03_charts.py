"""Build the charts in outputs/charts from the analysis outputs."""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
CH = OUT / "charts"
CH.mkdir(exist_ok=True, parents=True)

# Validated categorical slots 1-3 (blue, orange, aqua), sequential blue, neutral inks.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8985", "#e6e5e1", "#fcfcfb"
BLUE_LIGHT = "#a9c9f0"
INST_COLOR = {"UA": BLUE, "ASU": ORANGE, "NAU": AQUA}
INST_NAME = {"UA": "University of Arizona", "ASU": "Arizona State (Tempe)", "NAU": "Northern Arizona"}

for f in font_manager.findSystemFonts():
    if "Carlito" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": "Carlito", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURF,
    "axes.facecolor": SURF, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "savefig.facecolor": SURF,
})
SRC_IPEDS = "Source: IPEDS Fall Enrollment (residence of first-time freshmen) via Urban Institute Education Data API."
SRC_WICHE = "Source: WICHE, Knocking at the College Door, 11th ed. (2024), Projections Dataset."
SRC = ("Sources: IPEDS Fall Enrollment (residence of first-time freshmen) via Urban Institute Education Data API; "
       "WICHE, Knocking at the College Door, 11th ed. (2024).")

con = sqlite3.connect(ROOT / "data" / "processed" / "feeder.db")
mix = pd.read_csv(OUT / "residency_mix.csv")
mk = pd.read_csv(OUT / "market_ranking.csv")
scen = pd.read_csv(OUT / "scenarios_2025_2030.csv")


def finish(fig, ax, title, subtitle, name, source=SRC):
    fig.text(0.06, 0.965, title, fontsize=15, fontweight="bold", ha="left", va="top")
    fig.text(0.06, 0.915, subtitle, fontsize=10.5, color=INK2, ha="left", va="top")
    fig.text(0.06, 0.012, source, fontsize=7.5, color=MUTED, ha="left", va="bottom")
    fig.savefig(CH / name, dpi=200)
    plt.close(fig)


def hgrid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# 1. Out-of-state share by institution ---------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.09, right=0.80)
hgrid(ax)
for inst in ("UA", "ASU", "NAU"):
    d = mix[mix.inst == inst]
    ax.plot(d.year, 100 * d.out_of_state_share, color=INST_COLOR[inst], lw=2, marker="o", ms=7,
            markeredgecolor=SURF, markeredgewidth=2, label=INST_NAME[inst])
    last = d.iloc[-1]
    ax.text(2024.15, 100 * last.out_of_state_share, f"{INST_NAME[inst]}  {100*last.out_of_state_share:.0f}%",
            va="center", color=INK, fontsize=10)
ax.set_xticks([2018, 2022, 2024]); ax.set_xlim(2017.6, 2024.1)
ax.set_ylim(0, 60); ax.set_ylabel("Out-of-state U.S. residents, % of first-time freshmen")
ax.legend(loc="lower left", frameon=False, fontsize=9.5)
finish(fig, ax, "Arizona draws the largest out-of-state share of the three in-state publics",
       "Share of first-time degree-seeking freshmen who live in another U.S. state (fall of each year)",
       "01_out_of_state_share.png", SRC_IPEDS)

# 2. Top 15 UA out-of-state markets, 2024 ------------------------------------
top = mk.sort_values("ua_2024", ascending=False).head(15).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 5.8))
fig.subplots_adjust(top=0.86, bottom=0.12, left=0.11, right=0.95)
hgrid(ax, "x")
ax.barh(top.state, top.ua_2024, color=BLUE, height=0.62)
ax.scatter(top.ua_2018, top.state, color=INK, s=22, zorder=3, label="Fall 2018")
for s, v, v18 in zip(top.state, top.ua_2024, top.ua_2018):
    ax.text(max(v, v18) + 18, s, f"{int(v):,}", va="center", fontsize=9.5, color=INK2)
ax.set_xlabel("First-time freshmen at the University of Arizona, fall 2024")
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Line2D([], [], marker="o", color=INK, ls="", ms=5)],
          labels=["Fall 2024", "Fall 2018"], loc="lower right", frameon=False, fontsize=9.5)
ax.set_xlim(0, 1200)
finish(fig, ax, "California supplies 27% of Arizona's out-of-state freshmen",
       "Top 15 states by first-time freshmen, fall 2024 (bars) against fall 2018 (dots)",
       "02_top_markets.png", SRC_IPEDS)

# 3. Pool size vs traction ---------------------------------------------------
fig, ax = plt.subplots(figsize=(8.2, 5.8))
fig.subplots_adjust(top=0.84, bottom=0.13, left=0.10, right=0.96)
hgrid(ax, "both")
x = mk.ua_per_1000.clip(lower=0.05)
ax.scatter(x, mk.grads_avg_2025_2030, s=np.sqrt(mk.ua_2024.clip(lower=1)) * 9, color=BLUE, alpha=0.75,
           edgecolor=SURF, linewidth=1.5, zorder=3)
agg24 = pd.read_csv(OUT / "ua_out_of_state_rate_by_year.csv").set_index("year").loc[2024, "per_1000"]
big = mk.grads_avg_2025_2030.quantile(0.75)
ax.axvline(agg24, color=MUTED, lw=1, ls=(0, (4, 3))); ax.axhline(big, color=MUTED, lw=1, ls=(0, (4, 3)))
ax.set_xscale("log"); ax.set_yscale("log")
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
ax.xaxis.set_major_locator(FixedLocator([0.1, 0.2, 0.5, 1, 2, 5]))
ax.xaxis.set_major_formatter(FixedFormatter(["0.1", "0.2", "0.5", "1", "2", "5"]))
ax.yaxis.set_major_locator(FixedLocator([10000, 20000, 50000, 100000, 200000, 400000]))
ax.yaxis.set_major_formatter(FixedFormatter(["10k", "20k", "50k", "100k", "200k", "400k"]))
ax.xaxis.set_minor_locator(NullLocator()); ax.yaxis.set_minor_locator(NullLocator())
ax.set_xlim(0.1, 8)
label = ["TX", "CA", "FL", "NY", "IL", "PA", "OH", "NC", "GA", "NJ", "VA", "WA", "CO", "ID", "MN", "MI", "IN", "NV"]
for _, r in mk[mk.state.isin(label)].iterrows():
    ax.annotate(r.state, (max(r.ua_per_1000, 0.05), r.grads_avg_2025_2030), xytext=(5, 4),
                textcoords="offset points", fontsize=9.5, color=INK)
ax.text(agg24 * 1.05, ax.get_ylim()[0] * 1.15, f"UA out-of-state average {agg24:.2f}", fontsize=8.5, color=INK2)
ax.text(0.105, big * 1.06, "Top quartile of graduate pools", fontsize=8.5, color=INK2)
ax.set_xlabel("UA freshmen per 1,000 high school graduates, 2024 (log scale)")
ax.set_ylabel("Average projected graduates, 2025 to 2030 (log scale)")
finish(fig, ax, "Texas, Florida and New Jersey: big pools where Arizona has little traction",
       "Each dot is one state; dot size is UA freshmen in 2024. Dashed lines mark the UA average rate and the top-quartile pool",
       "03_pool_vs_traction.png")

# 4. Peer benchmark ----------------------------------------------------------
peer = pd.read_csv(OUT / "peer_benchmark_top15_pools.csv").head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 6))
fig.subplots_adjust(top=0.86, bottom=0.13, left=0.09, right=0.95)
hgrid(ax, "x")
h = 0.26
ypos = np.arange(len(peer))
for i, (inst, col) in enumerate((("ua_per_1000", BLUE), ("asu_per_1000", ORANGE), ("nau_per_1000", AQUA))):
    ax.barh(ypos + (1 - i) * h, peer[inst], height=h * 0.85, color=col,
            label={"ua_per_1000": "Arizona", "asu_per_1000": "ASU (Tempe)", "nau_per_1000": "NAU"}[inst])
ax.set_yticks(ypos); ax.set_yticklabels(peer.state)
ax.set_xlabel("First-time freshmen per 1,000 high school graduates, 2024")
ax.legend(loc="lower right", frameon=False, fontsize=10)
finish(fig, ax, "ASU enrolls more freshmen per graduate than Arizona in 8 of the 10 largest pools",
       "The ten largest graduate pools outside Arizona, ranked by average projected graduates 2025 to 2030",
       "04_peer_benchmark.png")

# 5. Outlook for top UA markets ----------------------------------------------
t = mk.sort_values("ua_2024", ascending=False).head(12).copy()
t["chg"] = 100 * t.outlook_2030
t = t.sort_values("chg")
fig, ax = plt.subplots(figsize=(8, 5.4))
fig.subplots_adjust(top=0.86, bottom=0.14, left=0.09, right=0.93)
hgrid(ax, "x")
ax.barh(t.state, t.chg, color=[ORANGE if v < 0 else BLUE for v in t.chg], height=0.62)
for s, v in zip(t.state, t.chg):
    ax.text(v + (0.3 if v >= 0 else -0.3), s, f"{v:+.1f}%", va="center", ha="left" if v >= 0 else "right",
            fontsize=9.5, color=INK2)
ax.axvline(0, color=INK2, lw=1)
ax.set_xlim(-16, 8)
ax.set_xlabel("Projected change in high school graduates, class of 2024 to class of 2030")
finish(fig, ax, "California, Arizona's top out-of-state market, is projected to lose 9% of graduates",
       "WICHE projection for the 12 states that sent the most freshmen to Arizona in 2024; orange = decline, blue = growth",
       "05_outlook_top_markets.png")

# 6. Scenarios ---------------------------------------------------------------
oos_hist = pd.read_csv(OUT / "ua_out_of_state_rate_by_year.csv")
base_2024 = int(oos_hist.set_index("year").loc[2024, "freshmen"])
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.74)
hgrid(ax)
lo = scen[scen.scenario == "low_observed_pooled_rate"].set_index("class_year").out_of_state
hi = scen[scen.scenario == "high_observed_pooled_rate"].set_index("class_year").out_of_state
yrs = [2024] + list(lo.index)
ax.fill_between(list(lo.index), list(lo), list(hi), color=BLUE_LIGHT, alpha=0.5, lw=0)
for name, col, ls, lab in (("hold_2024_state_rates", BLUE, "-", "Hold 2024 rates"),
                           ("whatif_top5_plus10pct", ORANGE, (0, (5, 3)), "What-if: top 5 markets +10%")):
    d = scen[scen.scenario == name].set_index("class_year").out_of_state
    ax.plot(yrs, [base_2024] + list(d), color=col, lw=2, ls=ls)
    ax.text(2030.15, d.iloc[-1], f"{lab}  {d.iloc[-1]:,.0f}", va="center", fontsize=9.5, color=INK)
ax.text(2030.15, hi.iloc[-1] + 70, f"Highest observed rate  {hi.iloc[-1]:,.0f}", va="center", fontsize=9, color=INK2)
ax.text(2030.15, lo.iloc[-1], f"Lowest observed rate  {lo.iloc[-1]:,.0f}", va="center", fontsize=9, color=INK2)
ax.scatter([2024], [base_2024], color=INK, s=34, zorder=4)
ax.text(2024.08, base_2024 - 190, f"2024 actual  {base_2024:,}", fontsize=9.5, color=INK)
ax.set_ylim(2500, 4700); ax.set_xlim(2023.8, 2030.1)
ax.set_xticks(range(2024, 2031))
ax.set_ylabel("Out-of-state first-time freshmen (49 states and DC)")
finish(fig, ax, "Arizona's recruiting rate moves out-of-state intake far more than demographics do",
       "Holding 2024 rates, projected graduates trim out-of-state freshmen about 5% by 2030.\nThe band spans the lowest to highest rate seen in 2018, 2022 and 2024.",
       "06_scenarios.png")

# 7. Arizona home pool -------------------------------------------------------
az = pd.read_csv(OUT / "arizona_hs_graduates.csv")
fig, ax = plt.subplots(figsize=(8, 4.8))
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.10, right=0.95)
hgrid(ax)
act = az[az.class_year <= 2023]; prj = az[az.class_year >= 2023]
ax.plot(act.class_year, act.hs_graduates / 1000, color=BLUE, lw=2, label="Reported, with some projected values")
ax.plot(prj.class_year, prj.hs_graduates / 1000, color=BLUE, lw=2, ls=(0, (5, 3)), label="WICHE projection")
pk = az.loc[az.hs_graduates.idxmax()]
ax.scatter([pk.class_year], [pk.hs_graduates / 1000], color=INK, s=34, zorder=4)
ax.annotate(f"Peak {int(pk.class_year)}: {pk.hs_graduates/1000:.1f}k", (pk.class_year, pk.hs_graduates / 1000),
            xytext=(-95, 6), textcoords="offset points", fontsize=9.5, arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_ylim(60, 95); ax.set_ylabel("Arizona high school graduates (thousands)")
ax.set_xticks(range(2010, 2042, 5))
ax.legend(loc="upper left", frameon=False, fontsize=9.5)
finish(fig, ax, "Arizona's home pool grows to 2034, then falls back",
       "Public and private high school graduates, class of 2009 to class of 2041",
       "07_arizona_home_pool.png", SRC_WICHE)
print("charts written:", sorted(p.name for p in CH.iterdir()))
