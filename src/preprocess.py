# src/preprocess.py

import pandas as pd
from dateutil import parser
from langdetect import detect, DetectorFactory
import os

DetectorFactory.seed = 0  # ensure consistent language detection

def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

def clean_reviews():
    # Read raw CSV
    df = pd.read_csv("data/raw/raw_reviews.csv")

    # Drop missing review text
    df = df.dropna(subset=["review"])

    # Remove duplicates based on review text
    df = df.drop_duplicates(subset=["review"])

    # Remove empty reviews
    df = df[df["review"].str.strip() != ""]

    # Filter only English reviews
    df = df[df["review"].apply(is_english)]

    # Normalize dates to YYYY-MM-DD
    df["date"] = df["date"].apply(lambda x: parser.parse(str(x)).strftime("%Y-%m-%d"))

    # Reset index
    df.reset_index(drop=True, inplace=True)

    # Ensure cleaned folder exists
    os.makedirs("data/cleaned", exist_ok=True)

    # Save cleaned CSV
    cleaned_file = "data/cleaned/clean_reviews.csv"
    df.to_csv(cleaned_file, index=False, encoding="utf-8")

    print("Preprocessing complete. Saved to data/cleaned/clean_reviews.csv")
    print(f"Total reviews after cleaning: {len(df)}")

if __name__ == "__main__":
    clean_reviews()
