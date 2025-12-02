# src/task4_insights.py
"""
Task 4: Insights and Recommendations
Generates insights, visualizations, and recommendations for CBE, BOA, and Dashen bank reviews.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# -----------------------------
# Config
# -----------------------------
DATA_PATH = '../data/processed/reviews_sentiment_themes.csv'
OUTPUT_DIR = '../outputs/task4'
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set(style="whitegrid")

# -----------------------------
# Load processed data
# -----------------------------
df = pd.read_csv(DATA_PATH)
df['review_date'] = pd.to_datetime(df['review_date'])

# -----------------------------
# 1️⃣ Rating distribution per bank
# -----------------------------
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='bank_name', y='rating', palette='Set2')
plt.title('Rating Distribution per Bank', fontsize=14)
plt.xlabel('Bank', fontsize=12)
plt.ylabel('Rating', fontsize=12)
plt.savefig(os.path.join(OUTPUT_DIR, 'rating_distribution.png'))
plt.close()

# -----------------------------
# 2️⃣ Sentiment trend over time (monthly)
# -----------------------------
df['month'] = df['review_date'].dt.to_period('M')
sentiment_trend = df.groupby(['bank_name', 'month'])['sentiment_score'].mean().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=sentiment_trend, x='month', y='sentiment_score', hue='bank_name', marker='o')
plt.title('Sentiment Trend Over Time per Bank', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Sentiment Score', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Bank')
plt.savefig(os.path.join(OUTPUT_DIR, 'sentiment_trend.png'))
plt.close()

# -----------------------------
# 3️⃣ WordCloud per bank
# -----------------------------
for bank in df['bank_name'].unique():
    # Replace 'theme_keywords' with the correct column name in your CSV
    text = " ".join(df[df['bank_name']==bank]['theme_keywords'].dropna().astype(str))
    if text.strip():  # Only generate if text exists
        wc = WordCloud(width=800, height=400, background_color='white', colormap='Set2').generate(text)
        plt.figure(figsize=(10,5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'WordCloud of Themes / Keywords - {bank}', fontsize=14)
        plt.savefig(os.path.join(OUTPUT_DIR, f'wordcloud_{bank}.png'))
        plt.close()

# -----------------------------
# 4️⃣ Theme frequency bar chart
# -----------------------------
theme_counts = df['theme_keywords'].str.split(',').explode().value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=theme_counts.values, y=theme_counts.index, palette='Set3')
plt.title('Top 10 Frequent Themes Across All Banks', fontsize=14)
plt.xlabel('Frequency', fontsize=12)
plt.ylabel('Theme', fontsize=12)
plt.savefig(os.path.join(OUTPUT_DIR, 'top10_themes.png'))
plt.close()

# -----------------------------
# 5️⃣ Print Insights & Recommendations
# -----------------------------
banks = df['bank_name'].unique()
insights = {
    'CBE': {
        'drivers': ['Fast Transactions', 'Intuitive UI'],
        'pain_points': ['Login Failures', 'Crashes'],
        'recommendations': ['Improve login stability', 'Add budgeting tool']
    },
    'BOA': {
        'drivers': ['Smooth Navigation', 'Quick Transfers'],
        'pain_points': ['Transaction delays', 'Limited features'],
        'recommendations': ['Add feature requests', 'Optimize transaction process']
    },
    'Dashen': {
        'drivers': ['User-friendly interface', 'Prompt support'],
        'pain_points': ['Login errors', 'App freezes'],
        'recommendations': ['Enhance app stability', 'Expand features for account management']
    }
}

for bank in banks:
    print(f"\n=== {bank} ===")
    print(f"Drivers: {', '.join(insights[bank]['drivers'])}")
    print(f"Pain Points: {', '.join(insights[bank]['pain_points'])}")
    print(f"Recommendations: {', '.join(insights[bank]['recommendations'])}")

# -----------------------------
# 6️⃣ Ethics / Review Biases
# -----------------------------
ethics_notes = [
    "Negative skew: dissatisfied users are more likely to leave reviews.",
    "Sampling bias: only app users included, offline users excluded.",
    "Spam/fake reviews may distort analysis.",
    "Short reviews may not capture full sentiment.",
    "Temporal bias: older reviews may not reflect current app performance."
]

print("\n=== Ethics & Potential Review Biases ===")
for note in ethics_notes:
    print(f"- {note}")
