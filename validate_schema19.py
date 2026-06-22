from minio import Minio
import pandas as pd
from io import BytesIO

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

bucket = "sportsdata"

TARGET_SCHEMA = (
    "Financial year",
    "Industry",
    "Industry Code",
    "Quartile label",
    "Financial benchmark",
    "Value type",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason"
)

matched_files = []
bad_files = []

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
            nrows=5,
            dtype=str,
            low_memory=False
        )

        df.columns = [c.strip() for c in df.columns]

        if tuple(df.columns) == TARGET_SCHEMA:

            matched_files.append(
                obj.object_name
            )

            print(f"MATCH | {obj.object_name}")

    except Exception as e:

        bad_files.append(
            (obj.object_name, str(e))
        )

print("\n====================")
print("SCHEMA 19 VALIDATION")
print("====================")

print(f"\nMatching Files : {len(matched_files)}")
print(f"Bad Files      : {len(bad_files)}")

if matched_files:

    print("\nExample Files:\n")

    for file in matched_files[:10]:
        print(file)

if bad_files:

    print("\nErrors:\n")

    for file, err in bad_files:
        print(file)
        print(err)