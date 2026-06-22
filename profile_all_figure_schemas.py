from minio import Minio
import pandas as pd
from io import BytesIO
from collections import defaultdict

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

bucket = "sportsdata"

schema_groups = defaultdict(list)

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

        columns = tuple(df.columns)

        schema_groups[columns].append(obj.object_name)

    except Exception as e:
        print(f"Error: {obj.object_name}")
        print(e)

print("\n====================")
print("SCHEMA SUMMARY")
print("====================")

for i, (schema, files) in enumerate(schema_groups.items(), start=1):

    print(f"\nSchema {i}")
    print(f"Files: {len(files)}")

    print("Columns:")
    for col in schema:
        print(f"  - {col}")

    print("\nExample file:")
    print(files[0])