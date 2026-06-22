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

files = [
    "Figure.nz data/Chart Data/Amusement, fitness and sports centre managers in New Zealand.csv",
    "Figure.nz data/Chart Data/Amusement, fitness and sports centre managers in New Zealand (2).csv",
    "Figure.nz data/Chart Data/Sports coaches, instructors and officials in New Zealand.csv",
    "Figure.nz data/Chart Data/Sports coaches, instructors and officials in New Zealand (2).csv",
    "Figure.nz data/Chart Data/Sports coaches, instructors and officials in New Zealand (3).csv",
    "Figure.nz data/Chart Data/Sports coaches, instructors and officials in New Zealand (4).csv",
    "Figure.nz data/Chart Data/Sports coaches, instructors and officials in New Zealand (5).csv"
]

for f in files:

    try:
        response = client.get_object(bucket, f)

        df = pd.read_csv(
            BytesIO(response.read()),
            nrows=5
        )

        print("\n====================")
        print(f)
        print("====================")

        for col in df.columns:
            print(col)

    except Exception as e:
        print(f"\nERROR: {f}")
        print(e)