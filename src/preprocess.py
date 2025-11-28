import pandas as pd
from dateutil import parser

def clean_reviews():
    df = pd.read_csv("data/raw/raw_reviews.csv")

    # Drop missing review text
    df = df.dropna(subset=["review"])

    # Remove duplicates
    df = df.drop_duplicates(subset=["review", "rating", "date"])

    # Normalize dates to YYYY-MM-DD
    df["date"] = df["date"].apply(lambda x: parser.parse(str(x)).strftime("%Y-%m-%d"))

    # Remove empty reviews
    df = df[df["review"].str.strip() != ""]

    # Reset index
    df.reset_index(drop=True, inplace=True)

    df.to_csv("data/cleaned/clean_reviews.csv", index=False, encoding="utf-8")
    print("Preprocessing complete. Saved to data/cleaned/clean_reviews.csv")

if __name__ == "__main__":
    clean_reviews()
