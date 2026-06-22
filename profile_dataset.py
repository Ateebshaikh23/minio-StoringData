from minio import Minio
import pandas as pd
from io import BytesIO

client = Minio(
    "localhost:9000",
    access_key="user",
    secret_key="Ateeb@12345",
    secure=False
)

file_path = "Figure.nz data/Table Data/Sport - Participation in sport and active recreation among adults 2023.csv"

response = client.get_object(
    "sportsdata",
    file_path
)

df = pd.read_csv(BytesIO(response.read()))

print("\nColumns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

print("\nFirst 10 rows:")
print(df.head(10))