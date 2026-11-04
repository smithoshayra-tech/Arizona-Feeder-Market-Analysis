-- One row per institution, year and state of residence (50 states + DC only).
DROP VIEW IF EXISTS v_state_freshmen;
CREATE VIEW v_state_freshmen AS
SELECT i.short_name AS inst, r.unitid, r.year, s.state, s.state_name,
       r.first_time_freshmen AS freshmen
FROM ipeds_residence r
JOIN institution i ON i.unitid = r.unitid
JOIN state_ref  s ON s.fips   = r.residence_code;

-- Freshmen per 1,000 high school graduates from the same state, same year.
-- Fall freshmen are matched to that spring's graduating class (see README limits).
DROP VIEW IF EXISTS v_penetration;
CREATE VIEW v_penetration AS
SELECT f.inst, f.year, f.state, f.state_name, f.freshmen,
       w.hs_graduates,
       1000.0 * f.freshmen / w.hs_graduates AS per_1000_grads
FROM v_state_freshmen f
JOIN wiche_hs_grads w ON w.state = f.state AND w.class_year = f.year;

-- Residency mix for each institution and year.
DROP VIEW IF EXISTS v_residency_mix;
CREATE VIEW v_residency_mix AS
SELECT i.short_name AS inst, r.year,
       MAX(CASE WHEN r.residence_code = 99 THEN r.first_time_freshmen END) AS total_freshmen,
       MAX(CASE WHEN r.residence_code = 4  THEN r.first_time_freshmen END) AS arizona,
       MAX(CASE WHEN r.residence_code = 58 THEN r.first_time_freshmen END) AS us_total,
       MAX(CASE WHEN r.residence_code = 90 THEN r.first_time_freshmen END) AS foreign_residents
FROM ipeds_residence r JOIN institution i ON i.unitid = r.unitid
GROUP BY i.short_name, r.year;

-- Market table for the University of Arizona, one row per out-of-state market.
-- Grads outlook compares class of 2024 with the WICHE projections for 2030 and 2035.
DROP VIEW IF EXISTS v_market_base;
CREATE VIEW v_market_base AS
SELECT s.state, s.state_name,
  (SELECT freshmen FROM v_state_freshmen WHERE inst='UA'  AND year=2018 AND state=s.state) AS ua_2018,
  (SELECT freshmen FROM v_state_freshmen WHERE inst='UA'  AND year=2022 AND state=s.state) AS ua_2022,
  (SELECT freshmen FROM v_state_freshmen WHERE inst='UA'  AND year=2024 AND state=s.state) AS ua_2024,
  (SELECT freshmen FROM v_state_freshmen WHERE inst='ASU' AND year=2024 AND state=s.state) AS asu_2024,
  (SELECT freshmen FROM v_state_freshmen WHERE inst='NAU' AND year=2024 AND state=s.state) AS nau_2024,
  (SELECT hs_graduates FROM wiche_hs_grads WHERE state=s.state AND class_year=2024) AS grads_2024,
  (SELECT hs_graduates FROM wiche_hs_grads WHERE state=s.state AND class_year=2030) AS grads_2030,
  (SELECT hs_graduates FROM wiche_hs_grads WHERE state=s.state AND class_year=2035) AS grads_2035,
  (SELECT AVG(hs_graduates) FROM wiche_hs_grads WHERE state=s.state AND class_year BETWEEN 2025 AND 2030) AS grads_avg_2025_2030
FROM state_ref s
WHERE s.state <> 'AZ';
