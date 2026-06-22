from minio import Minio
import pandas as pd
from io import BytesIO

# --------------------------------
# MinIO Connection
# --------------------------------

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

bucket = "sportsdata"

# --------------------------------
# Schema 13 Definition
# --------------------------------

TARGET_SCHEMA = (
    "Year as at February",
    "Industry",
    "Industry Code",
    "Territorial authority",
    "Territorial authority Code",
    "Measure",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason"
)

matching_files = []
bad_files = []

print("\nScanning Figure.nz files...\n")

# --------------------------------
# Scan all Figure.nz files
# --------------------------------

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

        # Clean column names
        df.columns = [c.strip() for c in df.columns]

        if tuple(df.columns) == TARGET_SCHEMA:

            matching_files.append(
                obj.object_name
            )

            print(
                f"MATCH | {obj.object_name}"
            )

    except Exception as e:

        bad_files.append(
            obj.object_name
        )

        print(
            f"ERROR | {obj.object_name}"
        )

        print(e)

# --------------------------------
# Summary
# --------------------------------

print("\n====================")
print("SCHEMA 13 VALIDATION")
print("====================")

print(f"\nMatching Files : {len(matching_files)}")
print(f"Bad Files      : {len(bad_files)}")

print("\nExample Files:\n")

for file in matching_files[:10]:
    print(file)

print("\n====================")
print("VALIDATION COMPLETE")
print("====================")