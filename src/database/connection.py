import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

connection = psycopg.connect(
    host="localhost",
    port=5433,
    dbname=db_name,
    user=db_user,
    password=db_password
)

with connection.cursor() as cursor:
    cursor.execute("SELECT current_database();")
    result = cursor.fetchone()
    print("Connected to database:", result[0])

connection.close()