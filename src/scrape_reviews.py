from google_play_scraper import Sort, reviews
import pandas as pd

def scrape_bank_reviews(app_id, bank_name, count=500):
    all_reviews = []

    result, _ = reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=count
    )

    for r in result:
        all_reviews.append({
            "review": r.get("content", "").strip(),
            "rating": r.get("score"),
            "date": r.get("at"),
            "bank": bank_name,
            "source": "Google Play"
        })

    return pd.DataFrame(all_reviews)

def main():
    print("Scraping reviews...")

    apps = {
        "CBE": "com.combanketh.mobilebanking",
        "BOA": "com.boa.boaMobileBanking",
        "Dashen": "com.dashen.dashensuperapp"
    }

    df_list = []

    for bank, app_id in apps.items():
        print(f"Scraping {bank}...")
        df = scrape_bank_reviews(app_id, bank, count=500)
        df_list.append(df)

    final_df = pd.concat(df_list, ignore_index=True)
    final_df.to_csv("data/raw/raw_reviews.csv", index=False, encoding="utf-8")

    print("Scraping complete. Saved to data/raw/raw_reviews.csv")

if __name__ == "__main__":
    main()
