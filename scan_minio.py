from minio import Minio
import psycopg2
import os

# =========================
# MINIO CONFIG
# =========================

MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "user"
MINIO_SECRET_KEY = "Ateeb@12345"
BUCKET_NAME = "sportsdata"

# =========================
# POSTGRES CONFIG
# =========================

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="sport_nz_db",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

# =========================
# MINIO CLIENT
# =========================

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

print("Scanning bucket recursively...")

file_count = 0

# recursive=True is the important part
objects = client.list_objects(
    BUCKET_NAME,
    recursive=True
)

for obj in objects:

    object_path = obj.object_name

    file_name = os.path.basename(object_path)

    file_extension = os.path.splitext(file_name)[1].replace(".", "").lower()

    path_parts = object_path.split("/")

    source_folder = path_parts[0] if len(path_parts) > 0 else "unknown"

    cursor.execute(
        """
        INSERT INTO bronze.file_catalog (
            file_name,
            file_extension,
            source_folder,
            minio_path,
            file_size
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            file_name,
            file_extension,
            source_folder,
            object_path,
            obj.size
        )
    )

    file_count += 1

    if file_count % 100 == 0:
        print(f"Processed {file_count} files...")

conn.commit()

cursor.close()
conn.close()

print(f"\nCompleted!")
print(f"Total files loaded: {file_count}")