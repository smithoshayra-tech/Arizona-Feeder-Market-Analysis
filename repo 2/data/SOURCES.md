# Data sources and reconciliation

## IPEDS first-time freshmen by state of residence

Endpoint pattern (Urban Institute Education Data Portal, IPEDS Fall Enrollment, residence):

```
https://educationdata.urban.org/api/v1/college-university/ipeds/fall-enrollment/{year}/residence/?unitid={unitid}&type_of_freshman=1
```

Pulled for year in 2018, 2022, 2024 and unitid in 104179 (University of Arizona), 104151 (Arizona State University, Tempe), 105330 (Northern Arizona University). `type_of_freshman=1` is first-time degree-seeking students. Counts were copied from the JSON responses into `data/raw/ipeds_first_time_freshmen_by_residence.csv` (499 rows).

`residence_code` values:

| Code | Meaning |
|---|---|
| 1 to 56 | State or DC (FIPS) |
| 57 | State unknown |
| 58 | U.S. total |
| 89 | U.S. outlying areas total |
| 90 | Foreign |
| 98 | Adjustment (small negative values in some years; not used) |
| 99 | Grand total |

Reconciliation rules checked for every institution and year: states and DC plus code 57 equal code 58; code 58 plus codes 89 and 90 equal code 99.

## WICHE Knocking at the College Door, 11th edition

File: Knocking-at-the-College-Door-11th-Edition-Projections-Dataset-12-11-2024.xlsx (sheet "Data"), https://www.wiche.edu/knocking/data/

Subset used: Grade = "High school graduates", SchoolSector = "Grand Total (public+private)", RaceEthnicity = "Total/any", 50 states and DC, class of 2009 to 2041. `data_status` keeps WICHE's own label (Reported/Actual, Includes Reported/Actual and Projected Values, or Projection).

License: CC BY-NC-SA 4.0. Required attribution is in the README.
