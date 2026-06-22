import time
from io import BytesIO, StringIO

import pandas as pd
import psycopg2
from minio import Minio

# ─────────────────────────────────────────
# Connections
# ─────────────────────────────────────────

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="sport_nz_db",
    user="postgres",
    password="postgres",
)
cursor = conn.cursor()

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False,
)

bucket = "sportsdata"

# ─────────────────────────────────────────
# Schema definition
# ─────────────────────────────────────────

TARGET_SCHEMA = (
    "Year ended June",
    "Local authority",
    "Local authority Code",
    "Activity",
    "Income and expenditure item",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason",
    "Metadata 1",
    "Metadata 2",
)

# Postgres column order (must match bronze.figure_schema_25 table definition)
DB_COLUMNS = (
    "source_file",
    "year_ended_june",
    "local_authority",
    "local_authority_code",
    "activity",
    "income_expenditure_item",
    "value",
    "value_unit",
    "value_label",
    "null_reason",
    "metadata_1",
    "metadata_2",
)

COPY_SQL = f"""
    COPY bronze.figure_schema_25 ({', '.join(DB_COLUMNS)})
    FROM STDIN
    WITH (FORMAT CSV, NULL '')
"""

# ─────────────────────────────────────────
# Main loader
# ─────────────────────────────────────────

loaded_rows = 0
loaded_files = 0
total_start = time.perf_counter()

try:
    objects = client.list_objects(bucket, prefix="Figure.nz data/", recursive=True)

    for obj in objects:
        if not obj.object_name.lower().endswith(".csv"):
            continue

        print(f"\nChecking: {obj.object_name}")
        file_start = time.perf_counter()

        try:
            # ── Download ──────────────────────────────────────────────────
            t0 = time.perf_counter()
            response = client.get_object(bucket, obj.object_name)
            raw_bytes = response.read()
            t_download = time.perf_counter() - t0

            # ── Read & schema check ───────────────────────────────────────
            t0 = time.perf_counter()
            df = pd.read_csv(BytesIO(raw_bytes), dtype=str, low_memory=False)
            df.columns = [c.strip() for c in df.columns]
            t_read = time.perf_counter() - t0

            if tuple(df.columns) != TARGET_SCHEMA:
                continue

            print(f"  MATCH: {obj.object_name}")

            # ── FIX 1: Vectorized transform (replaces iterrows loop) ───────
            # Before: for _, row in df.iterrows(): rows.append(tuple(...))
            #         → Python loop over every row = very slow for 480k rows
            # After:  insert source_file column once, dump whole array at once
            t0 = time.perf_counter()

            df = df.where(pd.notnull(df), None)        # NaN → None (vectorized)
            df.insert(0, "source_file", obj.object_name)  # add column once

            # Convert entire DataFrame to CSV string in memory in one shot
            buffer = StringIO()
            df.to_csv(buffer, index=False, header=False, na_rep="")
            buffer.seek(0)

            t_transform = time.perf_counter() - t0

            # ── FIX 2: PostgreSQL COPY (replaces execute_values INSERT) ────
            # COPY streams data into Postgres as a bulk file load.
            # No row-by-row SQL parsing — Postgres reads it like a file import.
            t0 = time.perf_counter()
            cursor.copy_expert(COPY_SQL, buffer)
            conn.commit()
            t_load = time.perf_counter() - t0

            # ── Stats ─────────────────────────────────────────────────────
            loaded_files += 1
            loaded_rows += len(df)
            t_total_file = time.perf_counter() - file_start

            print(
                f"  SUCCESS | Files: {loaded_files} | "
                f"Rows: {loaded_rows:,} | "
                f"File time: {t_total_file:.1f}s "
                f"[dl={t_download:.2f}s  read={t_read:.2f}s  "
                f"transform={t_transform:.2f}s  copy={t_load:.2f}s]"
            )

        except Exception as e:
            conn.rollback()
            print(f"\n  FILE ERROR: {obj.object_name}")
            print(f"  {type(e).__name__}: {e}")

except Exception as e:
    print(f"\nFATAL ERROR: {type(e).__name__}: {e}")

finally:
    cursor.close()
    conn.close()

elapsed = time.perf_counter() - total_start
print("\n==============================")
print(f"Files Loaded : {loaded_files}")
print(f"Rows Loaded  : {loaded_rows:,}")
print(f"Total time   : {elapsed:.1f}s")
print(f"Avg per file : {elapsed / loaded_files:.1f}s" if loaded_files else "")
print("==============================")