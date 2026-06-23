from minio import Minio
import pandas as pd
from io import BytesIO

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

obj = client.get_object(
    "sportsdata",
    "Figure.nz data/Chart Data/Income and expenditure on recreation and sport by Auckland Council, New Zealand.csv"
)

df = pd.read_csv(BytesIO(obj.read()), nrows=5)

print("\nColumns:\n")

for c in df.columns:
    print(c)