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
    "Census year",
    "Subject population",
    "Age group",
    "Region",
    "Region Code",
    "Occupation",
    "Occupation Code",
    "Sex",
    "Unit",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason"
)

matching_files = []
bad_files = []

print("\nScanning Figure.nz files...\n")

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
            nrows=5
        )

        cols = tuple(df.columns)

        if cols == TARGET_SCHEMA:

            matching_files.append(obj.object_name)

            print(
                f"MATCH | {obj.object_name}"
            )

    except Exception:
        bad_files.append(obj.object_name)

print("\n====================")
print("SCHEMA 6 VALIDATION")
print("====================")

print(f"\nMatching Files : {len(matching_files)}")
print(f"Bad Files      : {len(bad_files)}")

print("\nExample Files:\n")

for f in matching_files[:10]:
    print(f)

print("\n====================")
print("VALIDATION COMPLETE")
print("====================")