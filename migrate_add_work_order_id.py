"""Add missing columns to trips table."""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

COLUMNS_TO_ADD = [
    ("work_order_id", "INTEGER REFERENCES work_orders(id)"),
    ("mine_id", "INTEGER REFERENCES mines(id)"),
    ("mines_qty", "NUMERIC(12, 2) DEFAULT 0.00"),
]


def migrate():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.autocommit = True
    cur = conn.cursor()

    for col_name, col_def in COLUMNS_TO_ADD:
        cur.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'trips' AND column_name = %s
        """, (col_name,))
        if cur.fetchone():
            print(f"Column {col_name} already exists, skipping.")
        else:
            print(f"Adding {col_name} column to trips table...")
            cur.execute(f"ALTER TABLE trips ADD COLUMN {col_name} {col_def}")
            print(f"Column {col_name} added successfully.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    migrate()
