import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> psycopg.Connection:
    """Open a new connection to the CareerOS Postgres database."""
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


if __name__ == "__main__":
    # Quick manual check: python -m src.database.connection
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            print("Connected to database:", cursor.fetchone()[0])