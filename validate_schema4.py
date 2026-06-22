from minio import Minio
import pandas as pd
from io import BytesIO

# -------------------
# MinIO
# -------------------

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

bucket = "sportsdata"

# -------------------
# Schema 4 Definition
# -------------------

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

matched_files = []
bad_files = []

objects = client.list_objects(
    bucket,
    prefix="Figure.nz data/",
    recursive=True
)

print("\nScanning Figure.nz files...\n")

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

            matched_files.append(obj.object_name)

            print(
                f"MATCH | {obj.object_name}"
            )

        else:

            pass

    except Exception as e:

        bad_files.append(
            (obj.object_name, str(e))
        )

print("\n========================")
print("SCHEMA 4 VALIDATION")
print("========================")

print(f"\nMatching Files : {len(matched_files)}")
print(f"Bad Files      : {len(bad_files)}")

if matched_files:

    print("\nFirst 10 Matching Files:\n")

    for file in matched_files[:10]:
        print(file)

if bad_files:

    print("\nErrors:\n")

    for file, err in bad_files:
        print(file)
        print(err)
        print("-" * 50)