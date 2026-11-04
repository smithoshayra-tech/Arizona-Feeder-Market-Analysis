"""Load the raw CSVs into SQLite and create the SQL views."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "feeder.db"


def load(con, table, csv_path, cols, casts):
    with open(csv_path, newline="") as f:
        rows = [tuple(c(r[k]) for k, c in zip(cols, casts)) for r in csv.DictReader(f)]
    con.executemany(f"INSERT INTO {table} VALUES ({','.join('?' * len(cols))})", rows)
    return len(rows)


def main():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.executescript((ROOT / "sql" / "01_schema.sql").read_text())
    raw = ROOT / "data" / "raw"
    n = {
        "institution": load(con, "institution", raw / "institutions.csv",
                            ["unitid", "short_name", "name"], [int, str, str]),
        "state_ref": load(con, "state_ref", raw / "state_reference.csv",
                          ["fips", "state", "state_name"], [int, str, str]),
        "ipeds_residence": load(con, "ipeds_residence",
                                raw / "ipeds_first_time_freshmen_by_residence.csv",
                                ["unitid", "year", "residence_code", "first_time_freshmen"],
                                [int, int, int, int]),
        "wiche_hs_grads": load(con, "wiche_hs_grads", raw / "wiche_hs_graduates_by_state.csv",
                               ["state", "class_year", "hs_graduates", "data_status"],
                               [str, int, int, str]),
    }
    con.executescript((ROOT / "sql" / "02_views.sql").read_text())
    con.commit()
    con.close()
    for t, c in n.items():
        print(f"{t}: {c} rows")


if __name__ == "__main__":
    main()
