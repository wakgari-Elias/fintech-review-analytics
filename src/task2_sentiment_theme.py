# src/task2_sentiment_theme.py
"""
Task-2 pipeline: sentiment analysis (DistilBERT) and thematic extraction (TF-IDF + rule mapping).
Inputs:
 - data/cleaned/clean_reviews.csv
Outputs:
 - data/processed/reviews_sentiment_themes.csv
 - data/processed/sentiment_summary.csv
 - data/processed/themes_keywords_by_bank.csv
"""

from transformers import pipeline
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy
# from task2_utils import is_english
from src.task2_utils import is_english


# Ensure reproducible progress bar behavior
tqdm.pandas()

# ---- CONFIG ----
INPUT_CLEAN = "data/cleaned/clean_reviews.csv"
OUT_DIR = "data/processed"
OUT_REVIEWS = os.path.join(OUT_DIR, "reviews_sentiment_themes.csv")
OUT_SUMMARY = os.path.join(OUT_DIR, "sentiment_summary.csv")
OUT_KEYWORDS = os.path.join(OUT_DIR, "themes_keywords_by_bank.csv")

DISTILBERT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
BATCH_SIZE = 32  # model batch size for inference

# ---- Ensure output dir exists ----
os.makedirs(OUT_DIR, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    """Load cleaned reviews CSV."""
    df = pd.read_csv(path)
    # Basic guard: ensure expected columns exist
    expected = {"review", "rating", "date", "bank", "source"}
    if not expected.issubset(set(df.columns)):
        raise ValueError(f"Input CSV must contain columns: {expected}")
    # Keep minimal columns
    return df[["review", "rating", "date", "bank", "source"]].copy()


def init_sentiment_model():
    """Initialize transformers sentiment pipeline (DistilBERT)."""
    # This will download model weights first time if not cached
    classifier = pipeline("sentiment-analysis", model=DISTILBERT_MODEL)
    return classifier


def compute_sentiment(df: pd.DataFrame, classifier) -> pd.DataFrame:
    """Apply classification in batches and add label/score columns."""
    reviews = df["review"].astype(str).tolist()
    labels = []
    scores = []

    # iterate in batches
    for i in range(0, len(reviews), BATCH_SIZE):
        batch = reviews[i : i + BATCH_SIZE]
        results = classifier(batch)
        for res in results:
            lab = res.get("label", "POSITIVE")
            score = float(res.get("score", 0.0))
            # map to numeric score: POSITIVE -> positive, NEGATIVE -> negative
            if lab == "NEGATIVE":
                numeric = -score
            else:
                numeric = score
            # apply a heuristic for NEUTRAL: low confidence near 0.5
            if score < 0.60:
                sentiment_label = "NEUTRAL"
                sentiment_score = 0.0
            else:
                sentiment_label = lab
                sentiment_score = numeric
            labels.append(sentiment_label)
            scores.append(sentiment_score)

    df["sentiment_label"] = labels
    df["sentiment_score"] = scores
    return df


def aggregate_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment by bank and rating."""
    agg = (
        df.groupby(["bank", "rating"])
        .agg(
            mean_sentiment_score=("sentiment_score", "mean"),
            positive_count=("sentiment_label", lambda x: (x == "POSITIVE").sum()),
            negative_count=("sentiment_label", lambda x: (x == "NEGATIVE").sum()),
            neutral_count=("sentiment_label", lambda x: (x == "NEUTRAL").sum()),
            n_reviews=("sentiment_label", "count"),
        )
        .reset_index()
    )
    return agg


def preprocess_for_tfidf(texts):
    """Minimal preprocess for TF-IDF: lowercase & remove extra spaces."""
    return [str(t).lower().strip() for t in texts]


def extract_tfidf_keywords(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Compute TF-IDF across the corpus grouped by bank.
    Return a DataFrame with bank and top keywords.
    """
    ngram_range = (1, 2)
    vectorizer = TfidfVectorizer(max_features=2000, ngram_range=ngram_range)
    df["clean_text"] = preprocess_for_tfidf(df["review"].tolist())

    keywords_rows = []
    for bank in df["bank"].unique():
        bank_texts = df.loc[df["bank"] == bank, "clean_text"].tolist()
        if not bank_texts:
            continue
        X = vectorizer.fit_transform(bank_texts)
        feature_names = vectorizer.get_feature_names_out()
        # sum TF-IDF over docs to get importance by corpus
        sums = np.asarray(X.sum(axis=0)).ravel()
        indices = sums.argsort()[::-1][:top_n]
        top_kw = [feature_names[i] for i in indices]
        keywords_rows.append({"bank": bank, "top_keywords": "; ".join(top_kw)})
    return pd.DataFrame(keywords_rows)


def map_keywords_to_themes(df_keywords: pd.DataFrame) -> dict:
    """
    Create a rule-based mapping of keywords to themes.
    This mapping is domain-specific and can be refined.
    """
    # Basic theme mapping based on frequent tokens
    mapping = {
        "login": "Account Access Issues",
        "password": "Account Access Issues",
        "otp": "Account Access Issues",
        "transfer": "Transaction Performance",
        "slow": "Transaction Performance",
        "delay": "Transaction Performance",
        "failed": "Transaction Performance",
        "crash": "Reliability & Stability",
        "bug": "Reliability & Stability",
        "ui": "User Interface & Experience",
        "interface": "User Interface & Experience",
        "design": "User Interface & Experience",
        "support": "Customer Support",
        "customer support": "Customer Support",
        "fingerprint": "Feature Requests",
        "feature": "Feature Requests",
        "payment": "Transaction Performance",
        "balance": "Account Information",
    }
    return mapping


def assign_themes_to_reviews(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Assign themes to each review using presence of mapped keywords."""
    # load spaCy for tokenization/lemmatization
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    theme_list = []

    # lower keys for matching
    lower_map = {k.lower(): v for k, v in mapping.items()}
    kw_set = list(lower_map.keys())

    for text in tqdm(df["review"].astype(str), desc="Assigning themes"):
        text_l = text.lower()
        assigned = set()
        # quick substring matching (fast and interpretable)
        for kw in kw_set:
            if kw in text_l:
                assigned.add(lower_map[kw])
        if not assigned:
            assigned.add("Other")
        theme_list.append("; ".join(sorted(assigned)))
    df["themes"] = theme_list
    return df


def main():
    """Run Task-2 pipeline end-to-end."""
    print("Loading cleaned reviews...")
    df = load_data(INPUT_CLEAN)

    # optional: ensure English only (most cleaned data already English)
    df = df[df["review"].apply(is_english)].reset_index(drop=True)

    # Sentiment
    print("Initializing sentiment model (this may take a moment)...")
    classifier = init_sentiment_model()
    print("Computing sentiment for reviews...")
    df = compute_sentiment(df, classifier)

    # Save intermediate
    df.to_csv(os.path.join(OUT_DIR, "reviews_with_sentiment.csv"),
              index=False, encoding="utf-8")

    # Aggregation
    print("Aggregating sentiment by bank and rating...")
    agg = aggregate_sentiment(df)
    agg.to_csv(OUT_SUMMARY, index=False, encoding="utf-8")

    # Thematic (keywords + rule mapping)
    print("Extracting top TF-IDF keywords per bank...")
    kw_df = extract_tfidf_keywords(df, top_n=30)
    kw_df.to_csv(OUT_KEYWORDS, index=False, encoding="utf-8")

    print("Mapping keywords to themes and assigning to reviews...")
    mapping = map_keywords_to_themes(kw_df)
    df = assign_themes_to_reviews(df, mapping)

    # Final save
    df.to_csv(OUT_REVIEWS, index=False, encoding="utf-8")
    print("Task-2 completed.")
    print(f"Wrote: {OUT_REVIEWS}")
    print(f"Wrote: {OUT_SUMMARY}")
    print(f"Wrote: {OUT_KEYWORDS}")


if __name__ == "__main__":
    main()
