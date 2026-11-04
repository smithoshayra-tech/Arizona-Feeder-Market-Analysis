# Where should the University of Arizona recruit? A feeder-market analysis

**Question.** Arizona fills almost half of its freshman class from other states, and that is the part of the class most exposed to changes in the number of high school graduates. Which out-of-state markets should an enrollment team prioritize, and how much does the graduate outlook alone change the class by 2030?

**Short answer.** Holding Arizona's 2024 recruiting rates constant, the projected graduate pool trims out-of-state freshmen from 3,823 to 3,638 by 2030 (down 185, or 4.8%). The swing in Arizona's own recruiting rate over 2018 to 2024 is about six times larger than that demographic drift. The markets that look strongest on pool size, outlook and current traction are California, Washington and Illinois (core), with Texas, Florida and New Jersey as the largest places where Arizona has little traction today.

## Findings

All figures are recomputed from the raw files in `src/04_validate.py` and listed in `outputs/validation_report.md`.

1. **Arizona leans on out-of-state students more than its in-state peers.** In fall 2024, 44.6% of Arizona's first-time freshmen came from other U.S. states, against 30.5% at Arizona State (Tempe) and 19.5% at Northern Arizona. Arizona's share was 41.2% in 2018 and 48.2% in 2022.

   ![Out-of-state share of first-time freshmen at Arizona, ASU and NAU](outputs/charts/01_out_of_state_share.png)
2. **One state carries a lot of weight.** California supplied 1,048 of Arizona's 3,823 out-of-state freshmen from the 50 states and DC in 2024 (27.4%). Washington (387) and Colorado (356) follow.

   ![Top 15 states by University of Arizona first-time freshmen](outputs/charts/02_top_markets.png)
3. **The graduate outlook hurts Arizona more than the national total suggests.** Graduates outside Arizona fall only 2.9% from the class of 2024 to the class of 2030. Arizona's freshmen from those states fall 4.8% at constant rates, because the states projected to shrink are where Arizona recruits best (California down 9.4%, Illinois down 12.5%, Colorado down 6.4%) and the states projected to grow are where it enrolls few (Texas up 3.4%, Florida up 1.9%). Arizona's own graduate pool is flat to 2030 (84,208 to 84,186) and peaks at 89,551 in 2034.

   ![Projected change in graduates 2024 to 2030, top 12 Arizona markets](outputs/charts/05_outlook_top_markets.png)

   ![Arizona high school graduates, class of 2009 to 2041](outputs/charts/07_arizona_home_pool.png)
4. **Recruiting rate matters more than demographics.** Arizona's pooled out-of-state rate was 0.82 freshmen per 1,000 graduates in 2018, 1.12 in 2022 and 1.04 in 2024. Applying the lowest and highest of those rates to the 2030 graduate pool gives 2,924 to 3,990 out-of-state freshmen, a spread of 1,066 against a demographic drift of 185.

   ![Out-of-state freshmen scenarios, 2025 to 2030](outputs/charts/06_scenarios.png)
5. **Arizona State converts more freshmen per graduate in 8 of the 10 largest pools.** Examples per 1,000 graduates in 2024: Texas 0.85 for ASU against 0.55 for Arizona, Pennsylvania 0.72 against 0.49, Ohio 0.35 against 0.25. Arizona is ahead in Florida, and the two tie in Georgia. Arizona also leads ASU in Washington (4.80 against 3.55) and Colorado (5.52 against 3.65).

   ![Freshmen per 1,000 graduates, Arizona, ASU and NAU, ten largest pools](outputs/charts/04_peer_benchmark.png)
6. **Market tiers.** Core (large pool, above-average Arizona traction): CA, WA, IL. Build (large pool, below-average traction): TX, NJ, FL, NC, VA, GA, PA, MI, NY, OH. Niche (smaller pool, strong traction): ID, MN, CO, DC, NV, IA, MT, NM, KS, AK, OR, HI. The full ranking is in `outputs/market_ranking.csv`.

   ![Graduate pool size against Arizona traction by state](outputs/charts/03_pool_vs_traction.png)
7. **What-if, labelled as an assumption.** A 10% relative lift in penetration in the five top-scoring markets (TX, WA, CA, NJ, FL) adds 171 freshmen in 2030 against holding rates (3,809 against 3,638), which nearly offsets the 185 lost to demographics. The 10% is a round number chosen for illustration, not a forecast of what recruiting spend would achieve.

## Method

- **Penetration.** Fall first-time freshmen from a state divided by that state's high school graduates (public and private) in the matching class year, per 1,000. IPEDS fall 2024 is matched to the class of 2024.
- **Priority score.** For each of the 50 non-Arizona markets, 0.4 times the percentile rank of average projected graduates 2025 to 2030, plus 0.3 times the percentile rank of projected change 2024 to 2030, plus 0.3 times the percentile rank of Arizona's freshmen per 1,000 graduates. **The weights are my assumption.** Under four alternative weightings the rank correlation with the base ranking runs from 0.60 to 0.96 and the overlap in the top 10 from 4 to 8 markets (`outputs/ranking_sensitivity.csv`). Read the ranking as one defensible ordering, not a finding. The tiers use two thresholds (top quartile of pool size, Arizona's pooled out-of-state rate) and depend on those choices too.
- **Scenarios.** Class years 2025 to 2030. Arizona in-state freshmen are the 2024 Arizona rate times projected Arizona graduates. Out-of-state freshmen use 2024 state-level rates ("hold"), or one pooled out-of-state rate set to the lowest or highest seen in 2018, 2022 and 2024, or the 10% what-if above.
- **Pipeline.** Raw CSVs load into SQLite (`sql/01_schema.sql`, `sql/02_views.sql`); `src/02_analysis.py` queries the views and scores the markets; `src/03_charts.py` draws the charts; `src/04_validate.py` recomputes the key figures from the raw files with pandas only and compares them with the SQL-driven outputs.

## Data

| Source | What | Years |
|---|---|---|
| IPEDS Fall Enrollment, residence of first-time students, through the Urban Institute Education Data Portal API | First-time degree-seeking freshmen by state of residence for the University of Arizona (unit 104179), Arizona State University Tempe (104151) and Northern Arizona University (105330) | Fall 2018, 2022, 2024 |
| WICHE, *Knocking at the College Door*, 11th edition (December 2024) | Public and private high school graduates by state, reported and projected | Class of 2009 to 2041 |

Exact request URLs and the reconciliation rules are in `data/SOURCES.md`.

WICHE attribution, as the file requires: Source: Western Interstate Commission for Higher Education, *Knocking at the College Door: Projections of High School Graduates*, 2024, www.wiche.edu/knocking. The dataset is licensed CC BY-NC-SA 4.0, so `data/raw/wiche_hs_graduates_by_state.csv` (a subset of it) carries the same terms.

## Limitations

- **Penetration is a proxy, not a yield rate.** IPEDS does not publish applications, admits or yield by state, so this project cannot say whether low traction in a state comes from awareness, price, admission policy or competitors.
- **Freshmen and graduates do not match exactly.** Some fall freshmen graduated in earlier years, and some graduates enroll elsewhere or not at all. Matching on the same year is an approximation.
- **Three years only.** IPEDS collects state of residence every other year. I used 2018, 2022 and 2024, so trends rest on three points, and 2020 is not included.
- **Small states are noisy.** In 14 markets Arizona enrolled fewer than 10 freshmen in 2024 (flagged `thin_evidence` in the ranking file), so their per-1,000 rates swing on a handful of students.
- **Missing IPEDS rows are treated as zero.** The tables list only states that sent at least one student.
- **Excluded from the totals above:** students with state unknown (13 at Arizona in 2024), U.S. outlying areas, and international students (293 at Arizona in 2024).
- **WICHE projections are projections.** Values from the class of 2024 onward are projected, and WICHE projects each state separately, so they may not sum to its national figure. Read the Technical Appendix before relying on a single state's number.
- **Scope.** ASU means the Tempe campus only. There is no tuition, net price, program mix or marketing cost data, so nothing here is a return-on-investment estimate.
- **Not causal.** The peer comparison shows where ASU enrolls more per graduate, not why.

## Run it

```
pip install -r requirements.txt
bash run_all.sh
```

This rebuilds the database, the output tables, the charts and the validation report from the CSVs in `data/raw`.

## Repository layout

```
data/raw/        source CSVs (IPEDS pulls, WICHE state subset, reference tables)
data/SOURCES.md  request URLs, row-code definitions, reconciliation rules
sql/             schema and views
src/             01 build database, 02 analysis, 03 charts, 04 validation
outputs/         CSV results, validation report, charts/
```

## How this was built

I built this with an AI assistant (Claude) for drafting code. The raw IPEDS counts were copied from the API responses into `data/raw/ipeds_first_time_freshmen_by_residence.csv` and then checked against IPEDS's own totals for every institution and year (`src/04_validate.py`, first 18 checks). Scoring weights, thresholds and the 10% what-if are choices, listed above, that a reader can change in `src/02_analysis.py`.

Author: Sharon Smith
