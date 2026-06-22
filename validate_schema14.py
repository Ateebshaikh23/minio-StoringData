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
    "Region",
    "Region Code",
    "Measure",
    "Value",
    "Value Unit",
    "Value Label",
    "Null Reason"
)

count = 0

for obj in client.list_objects(
    "sportsdata",
    prefix="Figure.nz data/",
    recursive=True
):

    if not obj.object_name.endswith(".csv"):
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

        df.columns = [c.strip() for c in df.columns]

        if tuple(df.columns) == TARGET_SCHEMA:

            count += 1
            print("MATCH |", obj.object_name)

    except:
        pass

print()
print("Schema 14 Files =", count)