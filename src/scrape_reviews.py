# src/scrape_reviews.py

from google_play_scraper import Sort, reviews
import pandas as pd
import time

# Function to scrape reviews for a single bank app
def scrape_bank_reviews(app_id, bank_name, target_count=450, batch_size=200):
    """
    Scrapes reviews for a single bank app from Google Play Store.
    Collects all reviews without language filtering.
    """
    all_reviews = []
    token = None
    attempts = 0

    print(f"Starting scrape for {bank_name}...")

    while len(all_reviews) < target_count and attempts < 10:
        result, token = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=token
        )

        if not result:
            print("No more reviews returned by API.")
            break

        for r in result:
            review_text = r.get("content", "").strip()
            if review_text:  # keep all reviews, even non-English
                all_reviews.append({
                    "review": review_text,
                    "rating": r.get("score"),
                    "date": r.get("at"),
                    "bank": bank_name,
                    "source": "Google Play"
                })
                if len(all_reviews) >= target_count:
                    break

        attempts += 1
        time.sleep(1)

    print(f"{bank_name}: {len(all_reviews)} reviews collected.")
    return pd.DataFrame(all_reviews)

# Main function to scrape all banks
def main():
    apps = {
        "CBE": {"app_id": "com.combanketh.mobilebanking", "target_count": 800},
        "BOA": {"app_id": "com.boa.boaMobileBanking", "target_count": 800},
        "Dashen": {"app_id": "com.dashen.dashensuperapp", "target_count": 800}
    }

    df_list = []

    for bank, info in apps.items():
        df = scrape_bank_reviews(
            info["app_id"],
            bank,
            target_count=info["target_count"]
        )
        df_list.append(df)

    final_df = pd.concat(df_list, ignore_index=True)

    # Save raw CSV
    final_df.to_csv("data/raw/raw_reviews.csv", index=False, encoding="utf-8")
    print("Scraping complete. Saved to data/raw/raw_reviews.csv")
    print(f"Total reviews collected: {len(final_df)}")

if __name__ == "__main__":
    main()
