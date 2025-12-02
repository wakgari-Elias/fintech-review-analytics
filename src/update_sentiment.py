import os
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

# Select reviews where sentiment is NULL
cur.execute("SELECT review_id, review_text FROM reviews WHERE sentiment_label IS NULL OR sentiment_score IS NULL;")
rows_to_update = cur.fetchall()

# Replace this with your actual sentiment analysis function
def sentiment_pipeline(text):
    # dummy example: positive if 'good' else negative
    if "good" in text.lower():
        return {"label": "positive", "score": 0.9}
    else:
        return {"label": "negative", "score": 0.1}

# Update the NULL sentiment rows
for review_id, review_text in rows_to_update:
    sentiment = sentiment_pipeline(review_text)
    cur.execute("""
        UPDATE reviews
        SET sentiment_label = %s,
            sentiment_score = %s
        WHERE review_id = %s;
    """, (sentiment["label"], sentiment["score"], review_id))

conn.commit()
cur.close()
conn.close()

print(f"Updated {len(rows_to_update)} reviews with sentiment values!")
