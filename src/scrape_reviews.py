# Library to scrape Google Play reviews
from google_play_scraper import Sort, reviews
import pandas as pd  # For data manipulation and storage
# For detecting language of reviews
from langdetect import detect, DetectorFactory
import time  # To add delays and avoid rate limits

DetectorFactory.seed = 0  # Ensure consistent language detection results

# Function to check if a review is in English


def is_english(text):
    try:
        return detect(text) == 'en'
    except BaseException:
        return False

# Function to scrape reviews for a single bank app


def scrape_bank_reviews(app_id, bank_name, target_count=450, batch_size=200):
    """
    Scrapes reviews for a single bank app from Google Play Store.
    Ensures at least target_count English reviews if possible.
    """
    all_reviews = []  # Store collected reviews
    token = None  # continuation token for pagination
    attempts = 0   # Safety counter to prevent infinite loop

    print(f"Starting scrape for {bank_name}...")

    # Loop until we collect enough English reviews or reach attempt limit
    while len(all_reviews) < target_count and attempts < 10:
        result, token = reviews(
            app_id,
            lang="en",  # Scrape English reviews
            country="us",  # Country context
            sort=Sort.NEWEST,  # Get newest reviews first
            count=batch_size,  # Number of reviews per batch
            continuation_token=token  # Token for pagination
        )

        if not result:
            print("No more reviews returned by API.")
            break

        # Process each review in the batch
        for r in result:
            # Get review text and remove extra spaces
            review_text = r.get("content", "").strip()
            if review_text and is_english(
                    review_text):  # Only keep English reviews
                all_reviews.append({
                    "review": review_text,
                    "rating": r.get("score"),  # Star rating
                    "date": r.get("at"),  # Review date
                    "bank": bank_name,  # Bank name
                    "source": "Google Play"  # Source of review
                })
                if len(all_reviews) >= target_count:  # Stop if target reached
                    break

        attempts += 1
        time.sleep(1)  # Polite delay to avoid rate limits

    print(f"{bank_name}: {len(all_reviews)} English reviews collected.")
    return pd.DataFrame(all_reviews)  # Convert list of reviews to DataFrame

# Main function to scrape all three banks


def main():
    apps = {
        "CBE": {"app_id": "com.combanketh.mobilebanking", "target_count": 500},
        "BOA": {"app_id": "com.boa.boaMobileBanking", "target_count": 450},
        "Dashen": {"app_id": "com.dashen.dashensuperapp", "target_count": 450}
    }

    df_list = []  # To store DataFrames for each bank

    # Loop through each bank and scrape reviews
    for bank, info in apps.items():
        df = scrape_bank_reviews(
            info["app_id"],
            bank,
            target_count=info["target_count"])
        df_list.append(df)

    # Combine all bank reviews into a single DataFrame
    final_df = pd.concat(df_list, ignore_index=True)
    # Save to CSV
    final_df.to_csv("data/raw/raw_reviews.csv", index=False, encoding="utf-8")

    print("Scraping complete. Saved to data/raw/raw_reviews.csv")
    print(f"Total English reviews collected: {len(final_df)}")


# Run main function when script is executed
if __name__ == "__main__":
    main()
