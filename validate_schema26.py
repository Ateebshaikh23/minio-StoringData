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
    "Metadata 2"
)

matching_files = []

print("\nScanning Figure.nz files...\n")

for obj in client.list_objects(
    "sportsdata",
    prefix="Figure.nz data/",
    recursive=True
):

    if not obj.object_name.lower().endswith(".csv"):
        continue

    try:
        response = client.get_object(
            "sportsdata",
            obj.object_name
        )

        df = pd.read_csv(
            BytesIO(response.read()),
            nrows=5
        )

        cols = tuple(df.columns)

        if cols == TARGET_SCHEMA:

            matching_files.append(
                obj.object_name
            )

            print(
                f"MATCH | {obj.object_name}"
            )

    except:
        pass

print("\n====================")
print("SCHEMA 26 VALIDATION")
print("====================")
print(f"\nMatching Files : {len(matching_files)}")

print("\nExample Files:\n")

for f in matching_files[:20]:
    print(f)