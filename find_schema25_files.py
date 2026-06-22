# find_schema25_files.py

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

target_schema = (
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

schema25_files = []

objects = client.list_objects(
    bucket,
    prefix="Figure.nz data/",
    recursive=True
)

for obj in objects:

    if not obj.object_name.lower().endswith(".csv"):
        continue

    try:
        response = client.get_object(bucket, obj.object_name)

        df = pd.read_csv(
            BytesIO(response.read()),
            nrows=5
        )

        if tuple(df.columns) == target_schema:
            schema25_files.append(obj.object_name)

    except Exception as e:
        print(f"Error: {obj.object_name}")

print(f"\nTotal Schema 25 files: {len(schema25_files)}")

with open("schema25_files.txt", "w", encoding="utf-8") as f:
    for file in schema25_files:
        f.write(file + "\n")