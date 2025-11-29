# fintech-review-analytics

# FinTech Review Analytics

A project to collect, preprocess, and analyze user reviews from banking apps on the Google Play Store. This project enables insights into customer satisfaction, pain points, and potential app improvements.

---

## Project Overview

**Goal:**  
Collect and analyze user feedback from three Ethiopian banks’ mobile apps—CBE, BOA, and Dashen Bank—to uncover trends in customer sentiment and common themes.

**Banks & Apps:**  
| Bank   | App ID | Google Play Link |
|--------|--------|-----------------|
| CBE    | com.combanketh.mobilebanking | [Link](https://play.google.com/store/apps/details?id=com.combanketh.mobilebanking&hl=en) |
| BOA    | com.boa.boaMobileBanking      | [Link](https://play.google.com/store/apps/details?id=com.boa.boaMobileBanking&hl=en) |
| Dashen | com.dashen.dashensuperapp     | [Link](https://play.google.com/store/apps/details?id=com.dashen.dashensuperapp&hl=en) |

---

## Task-1: Data Collection and Preprocessing

### 1. Web Scraping
- Uses `google-play-scraper` to collect reviews, ratings, review dates, and app names.
- Target: ≥400 reviews per bank (1,200+ total).
- Saved to `data/raw/raw_reviews.csv`.

### 2. Preprocessing
- Remove duplicates and missing values.
- Filter only English reviews.
- Normalize dates to `YYYY-MM-DD`.
- Save cleaned dataset to `data/cleaned/clean_reviews.csv`.

---

## Project Structure

```

fintech-review-analytics/
│
├─ src/
│  ├─ scrape_reviews.py      # Scrapes Google Play reviews
│  └─ preprocess.py          # Cleans and preprocesses scraped data
│
├─ data/
│  ├─ raw/                   # Raw scraped reviews
│  └─ cleaned/               # Cleaned, preprocessed reviews
│
├─ .gitignore
├─ requirements.txt
└─ README.md

````

---

## Usage

1. **Set up virtual environment (Python 3.12.10)**

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate      # Mac/Linux
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Scrape reviews**

```bash
python -m src.scrape_reviews
```

4. **Preprocess reviews**

```bash
python -m src.preprocess
```

---

## Continuous Integration (CI)

* Uses **Flake8** for Python linting.
* Code is formatted and checked for style compliance on every push.

---

## Deliverables

* `raw_reviews.csv`: Raw collected reviews.
* `clean_reviews.csv`: Deduplicated, English-only, date-normalized dataset.
* Flake8-compliant Python scripts ready for Task-2 (Sentiment & Thematic Analysis).

---

## KPIs for Task-1

* ≥1,200 reviews collected with <5% missing data.
* Clean CSV dataset stored.
* Git repository organized with clear commits and branch structure (`task-1` branch).

---

## Next Steps

* Task-2: Perform sentiment analysis and thematic extraction.
* Task-3: Store cleaned data in PostgreSQL.
* Task-4: Generate insights, visualizations, and recommendations.





