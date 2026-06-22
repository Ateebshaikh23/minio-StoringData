import time
from io import BytesIO, StringIO

import pandas as pd
import psycopg2
from minio import Minio

# ----------------------------------
# PostgreSQL
# ----------------------------------

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="sport_nz_db",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

# ----------------------------------
# MinIO
# ----------------------------------

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

bucket = "sportsdata"

# ----------------------------------
# Schema 4
# ----------------------------------

TARGET_SCHEMA = (
    "Year",
    "Survey question",
    "Response",
    "Grouping variable",
    "Category",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason",
    "Metadata 1"
)

DB_COLUMNS = (
    "source_file",
    "year",
    "survey_question",
    "response",
    "grouping_variable",
    "category",
    "value",
    "value_unit",
    "value_label",
    "null_reason",
    "metadata_1"
)

COPY_SQL = f"""
COPY bronze.figure_schema_4
({', '.join(DB_COLUMNS)})
FROM STDIN
WITH (
    FORMAT CSV,
    NULL ''
)
"""

loaded_files = 0
loaded_rows = 0

start_time = time.time()

objects = client.list_objects(
    bucket,
    prefix="Figure.nz data/",
    recursive=True
)

for obj in objects:

    if not obj.object_name.lower().endswith(".csv"):
        continue

    try:

        response = client.get_object(
            bucket,
            obj.object_name
        )

        df = pd.read_csv(
            BytesIO(response.read()),
            dtype=str,
            low_memory=False
        )

        df.columns = [c.strip() for c in df.columns]

        if tuple(df.columns) != TARGET_SCHEMA:
            continue

        print(f"\nLoading: {obj.object_name}")

        df = df.where(pd.notnull(df), "")

        df.insert(
            0,
            "source_file",
            obj.object_name
        )

        buffer = StringIO()

        df.to_csv(
            buffer,
            index=False,
            header=False
        )

        buffer.seek(0)

        cursor.copy_expert(
            COPY_SQL,
            buffer
        )

        conn.commit()

        loaded_files += 1
        loaded_rows += len(df)

        print(
            f"Loaded Files={loaded_files} Rows={loaded_rows:,}"
        )

    except Exception as e:

        conn.rollback()

        print("\nERROR")
        print(obj.object_name)
        print(type(e).__name__)
        print(e)

cursor.close()
conn.close()

print("\n====================")
print(f"Files Loaded : {loaded_files}")
print(f"Rows Loaded  : {loaded_rows:,}")
print(
    f"Time Taken   : {round(time.time()-start_time,2)} sec"
)
print("====================")