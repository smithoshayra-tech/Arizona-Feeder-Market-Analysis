-- Tables loaded from the raw CSVs by src/01_build_database.py
DROP TABLE IF EXISTS institution;
DROP TABLE IF EXISTS state_ref;
DROP TABLE IF EXISTS ipeds_residence;
DROP TABLE IF EXISTS wiche_hs_grads;

CREATE TABLE institution (
    unitid     INTEGER PRIMARY KEY,
    short_name TEXT NOT NULL,
    name       TEXT NOT NULL
);

CREATE TABLE state_ref (
    fips       INTEGER PRIMARY KEY,
    state      TEXT NOT NULL UNIQUE,
    state_name TEXT NOT NULL
);

-- IPEDS Fall Enrollment, residence of first-time degree-seeking freshmen.
-- residence_code: 1-56 = state or DC (FIPS), 57 = state unknown, 58 = U.S. total,
-- 89 = U.S. outlying areas total, 90 = foreign, 98 = adjustment, 99 = grand total.
CREATE TABLE ipeds_residence (
    unitid              INTEGER NOT NULL REFERENCES institution(unitid),
    year                INTEGER NOT NULL,
    residence_code      INTEGER NOT NULL,
    first_time_freshmen INTEGER NOT NULL,
    PRIMARY KEY (unitid, year, residence_code)
);

-- WICHE Knocking at the College Door, 11th ed.: public + private high school graduates.
CREATE TABLE wiche_hs_grads (
    state        TEXT NOT NULL REFERENCES state_ref(state),
    class_year   INTEGER NOT NULL,
    hs_graduates INTEGER NOT NULL,
    data_status  TEXT NOT NULL,
    PRIMARY KEY (state, class_year)
);
