from minio import Minio
import pandas as pd
from io import BytesIO

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

TARGET_SCHEMA = (
    "Year as at February",
    "Industry",
    "Industry Code",
    "Measure",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason"
)

bucket = "sportsdata"

matching = 0
bad = 0

objects = client.list_objects(
    bucket,
    prefix="Figure.nz data/",
    recursive=True
)

for obj in objects:

    if not obj.object_name.endswith(".csv"):
        continue

    try:

        response = client.get_object(
            bucket,
            obj.object_name
        )

        df = pd.read_csv(
            BytesIO(response.read()),
            nrows=5
        )

        cols = tuple(df.columns)

        if cols == TARGET_SCHEMA:

            matching += 1
            print(f"MATCH | {obj.object_name}")

        else:
            pass

    except Exception:
        bad += 1

print()
print("====================")
print("SCHEMA 15 VALIDATION")
print("====================")
print(f"Matching Files : {matching}")
print(f"Bad Files      : {bad}")