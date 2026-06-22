import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="sport_nz_db",
        user="postgres",
        password="postgres"
    )

    print("Connected Successfully!")

    conn.close()

except Exception as e:
    print("ERROR:")
    print(e)