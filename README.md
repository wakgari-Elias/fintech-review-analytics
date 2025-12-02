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



# 🚀 **Task 3 & Task 4 – Data Storage, Insights, and Visualizations**

This section summarizes the work completed for **Task 3** (PostgreSQL storage) and **Task 4** (Insights & Recommendations) as part of the Fintech Review Analytics project.
The goal of these tasks is to move from *cleaned review data* → *persistent storage* → *analysis, insights, and visuals*.

---

# 🗄️ **Task 3 – Store Cleaned Data in PostgreSQL**

### ✔ **Objective**

Design and implement a PostgreSQL database to store the cleaned and processed mobile banking reviews.

### ✔ **Steps Completed**

---

### **1. PostgreSQL Setup**

* Installed PostgreSQL locally (v18).
* Created a new database:

```sql
CREATE DATABASE bank_reviews;
```

---

### **2. Database Schema**

#### **Banks Table**

Stores bank metadata.

| Column    | Type               | Description     |
| --------- | ------------------ | --------------- |
| bank_id   | SERIAL PRIMARY KEY | Unique ID       |
| bank_name | VARCHAR(100)       | Bank name       |
| app_name  | VARCHAR(100)       | Mobile app name |

#### **Reviews Table**

Stores all cleaned reviews.

| Column          | Type                          | Description                   |
| --------------- | ----------------------------- | ----------------------------- |
| review_id       | SERIAL PRIMARY KEY            | Unique review ID              |
| bank_id         | INT REFERENCES banks(bank_id) | Link to bank                  |
| review_text     | TEXT                          | Cleaned review                |
| rating          | INT                           | User rating                   |
| review_date     | DATE                          | Review timestamp              |
| sentiment_label | VARCHAR(20)                   | Positive / Negative / Neutral |
| sentiment_score | FLOAT                         | Model-generated score         |
| source          | VARCHAR(50)                   | Google Play                   |

---

### **3. Data Insertion Script**

A Python script (`src/insert_reviews.py`) was created to insert cleaned reviews:

* Establishes connection via psycopg2.
* Inserts bank metadata.
* Inserts all cleaned reviews from:

```
data/cleaned/clean_reviews.csv
```

---

### **4. Data Verification Queries**

Examples:

```sql
-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id)
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- Average rating
SELECT bank_id, AVG(rating) FROM reviews GROUP BY bank_id;
```

---

# 📊 **Task 4 – Insights, Visualizations & Recommendations**

### ✔ **Objective**

Analyze sentiments, themes, and ratings to produce insights and improvement recommendations.

---

# 🔍 **1. Insights per Bank**

### **Example Deliverables (from the analysis)**

#### ⭐ **CBE**

* **Drivers:** Fast transactions, improved UI, quick notifications
* **Pain points:** Frequent login failures, crashes, slow loading

#### ⭐ **BOA**

* **Drivers:** Smooth UI, modern design
* **Pain points:** OTP delays, session timeouts

#### ⭐ **Dashen**

* **Drivers:** Reliable transfers, easy navigation
* **Pain points:** Update errors, app freezes

---

# 🔄 **2. Bank Comparison**

* CBE has **more negative reviews**, mainly performance issues.
* BOA shows **higher average ratings**, cleaner UX.
* Dashen is **balanced**, but struggles with stability after updates.

---

# 🎯 **3. Recommendations**

### **Per Bank (Example)**

#### **CBE**

* Improve authentication flow
* Add offline features for basic actions

#### **BOA**

* Enhance OTP reliability
* Simplify onboarding steps

#### **Dashen**

* Optimize update stability
* Improve crash reporting system

---

# 📈 **4. Visualizations**

Created inside:

```
notebooks/task4_insights.ipynb
```

### **Included Plots**

* Sentiment distribution per bank
* Rating distribution
* Sentiment trends over time
* Keyword/theme frequency
* WordClouds

All exported under:

```
outputs/task4/
```

---

# ⚖️ **5. Ethics & Bias Notice**

* Online reviews often contain **negative bias** (people complain more than praise).
* Some reviews may be **duplicates or spam**.
* App updates can cause **time-based sentiment shifts**.
* Sentiment model mistakes may affect results.

This section is included in the notebook.

---

# 📁 **Key Files for Task 3 & 4**

```
src/
│── insert_reviews.py     # Task 3 database insert script
│── task4_insights.py     # Task 4 insights + visualization code

notebooks/
│── task4_insights.ipynb  # Full analysis & plots

data/
│── cleaned/clean_reviews.csv
│── processed/*.csv

outputs/task4/*.png       # Saved charts
```









