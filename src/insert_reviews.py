# src/insert_reviews.py

import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100) NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50)
);
""")

conn.commit()

# Load cleaned CSV
df = pd.read_csv("data/cleaned/clean_reviews.csv")

# Insert unique banks first
banks = df[["bank"]].drop_duplicates()
for _, row in banks.iterrows():
    cur.execute("""
    INSERT INTO banks (bank_name, app_name)
    VALUES (%s, %s)
    ON CONFLICT (bank_name) DO NOTHING;
    """, (row["bank"], row["bank"] + " App"))

conn.commit()

# Map bank names to IDs
cur.execute("SELECT bank_id, bank_name FROM banks;")
bank_map = {name: id for id, name in cur.fetchall()}

# Insert reviews
for _, row in df.iterrows():
    cur.execute("""
    INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        bank_map[row["bank"]],
        row["review"],
        row["rating"],
        row["date"],
        row.get("sentiment_label", None),
        row.get("sentiment_score", None),
        row["source"]
    ))

conn.commit()
cur.close()
conn.close()

print("All reviews inserted successfully!")
