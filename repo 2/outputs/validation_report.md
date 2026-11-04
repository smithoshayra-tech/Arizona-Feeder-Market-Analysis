# Validation report

25 of 25 checks passed.

| Check | Result | Detail |
|---|---|---|
| IPEDS ASU 2018: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 8015+7 vs 8022 |
| IPEDS ASU 2018: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 8022+5+333 vs 8360 |
| IPEDS ASU 2022: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 13409+10 vs 13419 |
| IPEDS ASU 2022: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 13419+7+740 vs 14166 |
| IPEDS ASU 2024: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 12521+16 vs 12537 |
| IPEDS ASU 2024: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 12537+9+627 vs 13173 |
| IPEDS UA 2018: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 7180+51 vs 7231 |
| IPEDS UA 2018: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 7231+6+150 vs 7387 |
| IPEDS UA 2022: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 8234+11 vs 8245 |
| IPEDS UA 2022: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 8245+11+270 vs 8526 |
| IPEDS UA 2024: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 8299+13 vs 8312 |
| IPEDS UA 2024: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 8312+5+293 vs 8610 |
| IPEDS NAU 2018: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 5433+1 vs 5434 |
| IPEDS NAU 2018: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 5434+5+14 vs 5453 |
| IPEDS NAU 2022: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 5295+0 vs 5295 |
| IPEDS NAU 2022: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 5295+0+8 vs 5303 |
| IPEDS NAU 2024: states + DC + 'unknown state' = U.S. total (row 58) | PASS | 4676+0 vs 4676 |
| IPEDS NAU 2024: U.S. total + outlying areas + foreign = grand total (row 99) | PASS | 4676+0+9 vs 4685 |
| WICHE: 51 jurisdictions x 33 class years, no duplicates | PASS | 1683 rows |
| Market table: UA 2024 freshmen per state match the raw file (50 markets) | PASS |  |
| Market table: projected change 2024 to 2030 matches the raw WICHE file | PASS |  |
| Market table: UA freshmen per 1,000 graduates matches independent calculation | PASS |  |
| Priority score: independent recomputation equals stored score | PASS |  |
| Scenario hold-2024-rates, 2030 out-of-state: independent value equals stored | PASS | 3637.9 |
| 2024 out-of-state baseline (49 states + DC) = sum of state rows | PASS | 3823 |

## Figures quoted in the README and chart titles

```
{
 "out_of_state_share_2024_UA": 44.6,
 "out_of_state_share_2024_ASU": 30.5,
 "out_of_state_share_2024_NAU": 19.5,
 "ua_out_of_state_share_2018_2022_2024": [
  41.2,
  48.2,
  44.6
 ],
 "ca_share_of_ua_out_of_state_2024": 27.4,
 "ca_outlook_2030_pct": -9.4,
 "il_outlook_2030_pct": -12.5,
 "out_of_state_grads_change_2024_2030_pct": -2.94,
 "az_grads_2024_2030_2034_2041": [
  84208,
  84186,
  89551,
  81428
 ],
 "hold_rate_2030_out_of_state": 3638,
 "hold_vs_2024_pct": -4.8,
 "hold_vs_2024_delta": -185,
 "whatif_2030": 3809,
 "whatif_gain_vs_hold_2030": 171,
 "low_high_2030": [
  2924,
  3990
 ],
 "pooled_rates_2018_2022_2024": [
  0.818,
  1.116,
  1.037
 ],
 "top10_pools": [
  "CA",
  "TX",
  "FL",
  "NY",
  "OH",
  "PA",
  "IL",
  "GA",
  "NC",
  "NJ"
 ],
 "asu_above_ua_in_top10": 8,
 "asu_equal_ua_in_top10": [
  "GA"
 ],
 "top5_score": [
  "TX",
  "WA",
  "CA",
  "NJ",
  "FL"
 ],
 "tiers": {
  "Build: large pool, below-average traction": [
   "TX",
   "NJ",
   "FL",
   "NC",
   "VA",
   "GA",
   "PA",
   "MI",
   "NY",
   "OH"
  ],
  "Core: large pool, strong traction": [
   "WA",
   "CA",
   "IL"
  ],
  "Monitor": [
   "TN",
   "MD",
   "MA",
   "WI",
   "NE",
   "MO",
   "SD",
   "UT",
   "SC",
   "CT",
   "IN",
   "ND",
   "OK",
   "LA",
   "AL",
   "DE",
   "AR",
   "WY",
   "VT",
   "NH",
   "KY",
   "ME",
   "RI",
   "WV",
   "MS"
  ],
  "Niche: smaller pool, strong traction": [
   "ID",
   "MN",
   "CO",
   "DC",
   "NV",
   "IA",
   "MT",
   "NM",
   "KS",
   "AK",
   "OR",
   "HI"
  ]
 },
 "sensitivity": {
  "equal": {
   "spearman_vs_base": 0.96,
   "top10_overlap_with_base": 7.0
  },
  "pool_heavy": {
   "spearman_vs_base": 0.82,
   "top10_overlap_with_base": 8.0
  },
  "outlook_heavy": {
   "spearman_vs_base": 0.6,
   "top10_overlap_with_base": 5.0
  },
  "traction_heavy": {
   "spearman_vs_base": 0.71,
   "top10_overlap_with_base": 4.0
  }
 },
 "thin_markets": [
  "SD",
  "SC",
  "ND",
  "OK",
  "LA",
  "AL",
  "DE",
  "AR",
  "WY",
  "VT",
  "ME",
  "RI",
  "WV",
  "MS"
 ],
 "ua_top3_2024": {
  "CA": 1048,
  "WA": 387,
  "CO": 356
 }
}
```