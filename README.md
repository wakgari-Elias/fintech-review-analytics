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
  Here’s a detailed, clear, and professional README draft for **Task-2: Sentiment and Thematic Analysis**. You can copy and paste it directly:



# Task 2: Sentiment and Thematic Analysis

## Overview

This task analyzes user reviews collected from Google Play for three Ethiopian banks: **CBE**, **BOA**, and **Dashen Bank**.
The goal is to **quantify sentiment** and **identify recurring themes** to uncover user satisfaction drivers and pain points.

---

## Objectives

1. Perform **sentiment analysis** on the collected reviews to determine if user feedback is positive, negative, or neutral.
2. Conduct **thematic analysis** to group user concerns and highlights into actionable categories.
3. Provide insights that can guide **product improvement**, **customer support**, and **user experience** strategies.

---

## Approach

### 1. Sentiment Analysis

* Used the **`distilbert-base-uncased-finetuned-sst-2-english`** model from Hugging Face Transformers for accurate sentiment scoring.
* Optionally, simpler methods such as **VADER** or **TextBlob** can be used for comparison.
* Sentiment is aggregated by **bank** and **rating** to evaluate satisfaction across different review scores.
* Outputs include:

  * `review_id`
  * `review_text`
  * `sentiment_label` (`positive`, `negative`, `neutral`)
  * `sentiment_score` (probability/confidence)

### 2. Thematic Analysis

* Extracted keywords and key phrases using **TF-IDF** and **spaCy**.

* Grouped similar keywords into **3–5 themes per bank**, e.g.:

  * Account Access Issues
  * Transaction Performance
  * User Interface & Experience
  * Customer Support
  * Feature Requests

* Pipeline steps:

  1. Preprocessing: tokenization, stop-word removal, lemmatization
  2. Keyword extraction
  3. Manual/rule-based clustering into themes

* Outputs include:

  * `identified_theme(s)` for each review

---

## Folder Structure

```
.
├── data/
│   ├── cleaned/clean_reviews.csv      # Cleaned reviews used for analysis
│   └── analysis_results.csv           # Sentiment and themes output
├── src/
│   ├── sentiment_analysis.py          # Sentiment scoring script
│   ├── thematic_analysis.py           # Theme extraction script
│   └── preprocess.py                  # Preprocessing script
├── requirements.txt
└── README.md
```

---

## Usage

1. **Activate virtual environment:**

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
# or
source .venv/bin/activate       # Linux/Mac
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run sentiment analysis:**

```bash
python -m src.sentiment_analysis
```

4. **Run thematic analysis:**

```bash
python -m src.thematic_analysis
```

5. **Outputs**:

* `analysis_results.csv` contains:

  ```
  review_id | review_text | sentiment_label | sentiment_score | identified_theme(s)
  ```

---

## KPIs

* Sentiment scored for **90%+ reviews**.
* **3+ themes per bank** with representative keywords/examples.
* Modular and reusable pipeline.
* CSV output ready for reporting and visualization.

---

## Git & Branching

* All Task-2 code is developed in the **`task-2` branch**.
* Frequent commits ensure traceability:

  * Adding preprocessing
  * Adding sentiment analysis
  * Adding thematic analysis
  * Updating README & results

---

## Notes

* Requires cleaned reviews CSV from **Task-1**.
* Designed to be **modular**, so each analysis step can be run independently.
* Sentiment model can be swapped for experimentation with **VADER/TextBlob**.








