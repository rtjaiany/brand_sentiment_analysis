"""
NLP Sentiment Analysis and Text Mining Engine for Reddit Controversy Comments

This script performs advanced Natural Language Processing (NLP) on scraped Reddit comments:
1. VADER & TextBlob Sentiment Analysis (Compound, Pos, Neu, Neg, Subjectivity, Polarity)
2. Rule-based Emotion & Stance Categorization (Anger, Disgust, Support, Fear, Neutral)
3. N-Gram & Keyphrase Frequency Analysis (Unigrams, Bigrams, Trigrams)
4. Topic Modeling using Latent Dirichlet Allocation (LDA)
5. Upvote & Comment Depth Correlation Analysis
6. Visualization Generation (Saved to output/plots/)
7. Export to a NEW updated Excel Master File: output/master/Reddit_Master_Scraped_Comments_NLP.xlsx
"""

import os
import re
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud, STOPWORDS

# Configure matplotlib rendering style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("nlp_analysis.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Initialize VADER Analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Custom Stopwords
CUSTOM_STOPWORDS = set(STOPWORDS).union({
    "reddit", "com", "https", "http", "www", "post", "comment", "people",
    "think", "know", "say", "said", "one", "even", "would", "could", "get",
    "got", "like", "make", "going", "see", "also", "much", "well"
})


def clean_text_for_nlp(text: str) -> str:
    """Cleans raw comment text by removing URLs, special characters, and extra spaces."""
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove markdown links [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Replace multiple whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def compute_vader_sentiment(text: str) -> dict:
    """Computes VADER sentiment scores and categorical label."""
    if not text:
        return {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0, "label": "Neutral"}
    
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    scores['label'] = label
    return scores


def compute_textblob_metrics(text: str) -> dict:
    """Computes TextBlob subjectivity and polarity."""
    if not text:
        return {"subjectivity": 0.0, "polarity": 0.0}
    
    blob = TextBlob(text)
    return {
        "subjectivity": round(blob.sentiment.subjectivity, 4),
        "polarity": round(blob.sentiment.polarity, 4)
    }


def classify_emotion_tone(text: str, compound_score: float) -> str:
    """
    Classifies comment tone into core categories:
    - Anger / Outrage
    - Disgust / Criticism
    - Support / Loyalty
    - Fear / Concern
    - Skepticism / Neutral
    """
    if not text:
        return "Skepticism / Neutral"
    
    text_lower = text.lower()
    
    # Emotion Keyphrase Patterns
    anger_keywords = ["hate", "boycott", "outrage", "disgrace", "ridiculous", "idiot", "stupid", "garbage", "trash", "crap", "disgusting", "shame", "coward", "woke", "bigot", "fascist", "cancel", "scum"]
    criticism_keywords = ["fail", "caved", "backtrack", "hypocrite", "ruined", "drop", "stop", "terrible", "awful", "pander", "money", "greed", "mistake"]
    fear_keywords = ["fear", "scared", "threat", "violence", "danger", "warning", "afraid", "risk", "harm", "worry", "attack", "gun", "terror"]
    support_keywords = ["support", "love", "great", "good", "respect", "agree", "based", "right", "smart", "thank", "proud", "hero", "stand with"]

    has_anger = any(k in text_lower for k in anger_keywords)
    has_criticism = any(k in text_lower for k in criticism_keywords)
    has_fear = any(k in text_lower for k in fear_keywords)
    has_support = any(k in text_lower for k in support_keywords)

    if has_anger and compound_score < 0:
        return "Anger / Outrage"
    elif has_fear:
        return "Fear / Concern"
    elif has_criticism and compound_score < 0:
        return "Disgust / Criticism"
    elif has_support and compound_score > 0:
        return "Support / Loyalty"
    elif compound_score <= -0.5:
        return "Anger / Outrage"
    elif compound_score >= 0.5:
        return "Support / Loyalty"
    else:
        return "Skepticism / Neutral"


def extract_top_ngrams(texts: list, ngram_range=(2, 2), top_n=10) -> list:
    """Extracts top N-grams using CountVectorizer."""
    cleaned = [clean_text_for_nlp(t) for t in texts if isinstance(t, str) and len(t.strip()) > 5]
    if not cleaned:
        return []
    
    try:
        vec = CountVectorizer(ngram_range=ngram_range, stop_words='english', min_df=2)
        X = vec.fit_transform(cleaned)
        words = vec.get_feature_names_out()
        sums = X.sum(axis=0).A1
        freq_list = sorted(list(zip(words, sums)), key=lambda x: x[1], reverse=True)
        return freq_list[:top_n]
    except Exception as e:
        logging.debug(f"N-gram extraction exception: {e}")
        return []


def perform_topic_modeling(df_case: pd.DataFrame, n_topics=3, n_words=5) -> list:
    """Performs LDA Topic Modeling for a brand case."""
    texts = df_case['Comment Text'].dropna().apply(clean_text_for_nlp).tolist()
    if len(texts) < 10:
        return []
    
    try:
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        tfidf = vectorizer.fit_transform(texts)
        
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(tfidf)
        
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_features = [feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]]
            topics.append(f"Topic {topic_idx+1}: " + ", ".join(top_features))
        return topics
    except Exception as e:
        logging.warning(f"LDA Topic Modeling error: {e}")
        return []


def generate_visualizations(df: pd.DataFrame, output_dir="output/plots"):
    """Generates all 6 analytical charts and saves them to PNG files."""
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Generating NLP analytical charts in {output_dir}...")

    palette = {"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"}
    case_palette = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    # 1. Sentiment Distribution by Case (Stacked Bar Chart)
    plt.figure(figsize=(10, 6))
    sentiment_counts = pd.crosstab(df['Case'], df['Sentiment_Label'], normalize='index') * 100
    ax = sentiment_counts[['Positive', 'Neutral', 'Negative']].plot(
        kind='bar', stacked=True, color=['#2ecc71', '#bdc3c7', '#e74c3c'], figsize=(10, 6)
    )
    plt.title("Sentiment Distribution by Controversy Case (%)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Brand Case", fontsize=12)
    plt.ylabel("Percentage of Comments (%)", fontsize=12)
    plt.xticks(rotation=0, fontsize=11)
    plt.legend(title="Sentiment", frameon=True)
    for p in ax.patches:
        height = p.get_height()
        if height > 5:
            ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., p.get_y() + height / 2.),
                        ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_sentiment_distribution_by_case.png", dpi=300)
    plt.close()

    # 2. Sentiment by Top Subreddits (Grouped Bar Chart)
    plt.figure(figsize=(12, 6))
    top_subs = df['Subreddit'].value_counts().head(8).index
    df_top_subs = df[df['Subreddit'].isin(top_subs)]
    sns.countplot(data=df_top_subs, x='Subreddit', hue='Sentiment_Label', palette=palette, order=top_subs)
    plt.title("Sentiment Breakdown Across Top Subreddits", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Subreddit", fontsize=12)
    plt.ylabel("Comment Count", fontsize=12)
    plt.xticks(rotation=30, ha='right', fontsize=10)
    plt.legend(title="Sentiment")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_sentiment_by_subreddit.png", dpi=300)
    plt.close()

    # 3. Emotion Distribution by Case (Grouped Bar Chart)
    plt.figure(figsize=(12, 6))
    emotion_order = ["Anger / Outrage", "Disgust / Criticism", "Fear / Concern", "Support / Loyalty", "Skepticism / Neutral"]
    sns.countplot(data=df, x='Emotion_Tone', hue='Case', order=emotion_order, palette='Set2')
    plt.title("Emotion & Tone Distribution by Brand Controversy", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Emotion / Tone Category", fontsize=12)
    plt.ylabel("Comment Count", fontsize=12)
    plt.xticks(rotation=15, fontsize=10)
    plt.legend(title="Brand Case")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/03_emotion_distribution_by_case.png", dpi=300)
    plt.close()

    # 4. Upvote Score vs. Sentiment (Boxplot)
    plt.figure(figsize=(9, 6))
    # Filter score outliers for clean visualization (between -10 and 100)
    df_filtered_score = df[(df['Upvotes / Score'] >= -5) & (df['Upvotes / Score'] <= 150)]
    sns.boxplot(data=df_filtered_score, x='Sentiment_Label', y='Upvotes / Score', palette=palette, order=["Positive", "Neutral", "Negative"])
    plt.title("Comment Upvote Score Distribution by Sentiment", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Sentiment Label", fontsize=12)
    plt.ylabel("Upvotes / Score", fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/04_upvote_vs_sentiment.png", dpi=300)
    plt.close()

    # 5. Top Bigrams by Case (Horizontal Bar Charts)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    cases = df['Case'].unique()
    for idx, case in enumerate(cases):
        case_texts = df[df['Case'] == case]['Comment Text'].dropna().tolist()
        top_bigrams = extract_top_ngrams(case_texts, ngram_range=(2, 2), top_n=10)
        
        if top_bigrams:
            words, counts = zip(*top_bigrams)
            axes[idx].barh(words[::-1], counts[::-1], color='#3498db')
            axes[idx].set_title(f"Top Bigrams: {case}", fontsize=12, fontweight='bold')
            axes[idx].set_xlabel("Frequency", fontsize=10)
        else:
            axes[idx].text(0.5, 0.5, "No Bigrams Found", ha='center', va='center')
            
    plt.suptitle("Most Frequent Keyphrase Bigrams per Brand Controversy", fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/05_top_ngrams_by_case.png", dpi=300)
    plt.close()

    # 6. Word Clouds per Case
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for idx, case in enumerate(cases):
        case_text = " ".join(df[df['Case'] == case]['Comment Text'].dropna().apply(clean_text_for_nlp))
        wordcloud = WordCloud(width=600, height=400, background_color='white', stopwords=CUSTOM_STOPWORDS, colormap='Dark2').generate(case_text)
        axes[idx].imshow(wordcloud, interpolation='bilinear')
        axes[idx].axis("off")
        axes[idx].set_title(f"{case}", fontsize=14, fontweight='bold')
    plt.suptitle("Word Clouds of Comment Text per Brand Controversy", fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/06_wordcloud_by_case.png", dpi=300)
    plt.close()

    logging.info("All 6 charts generated successfully!")


def main():
    logging.info("Starting NLP Sentiment and Text Mining Engine...")

    master_input_path = "output/master/Reddit_Master_Scraped_Comments.xlsx"
    if not os.path.exists(master_input_path):
        logging.error(f"Input file not found at {master_input_path}")
        return

    # Load all sheets from original master workbook
    xls = pd.ExcelFile(master_input_path)
    dfs = []
    for sheet in xls.sheet_names:
        if sheet != "Summary":
            df_sheet = pd.read_excel(xls, sheet_name=sheet)
            dfs.append(df_sheet)

    if not dfs:
        logging.error("No valid data sheets found in workbook.")
        return

    df_full = pd.concat(dfs, ignore_index=True)
    logging.info(f"Loaded {len(df_full)} comments for NLP processing.")

    # Apply Clean Text
    df_full['Clean_Text'] = df_full['Comment Text'].apply(clean_text_for_nlp)

    # Compute Sentiment
    logging.info("Computing VADER & TextBlob sentiment metrics...")
    vader_results = df_full['Clean_Text'].apply(compute_vader_sentiment).apply(pd.Series)
    textblob_results = df_full['Clean_Text'].apply(compute_textblob_metrics).apply(pd.Series)

    df_full['Sentiment_Compound'] = vader_results['compound']
    df_full['Sentiment_Pos'] = vader_results['pos']
    df_full['Sentiment_Neu'] = vader_results['neu']
    df_full['Sentiment_Neg'] = vader_results['neg']
    df_full['Sentiment_Label'] = vader_results['label']
    df_full['Subjectivity'] = textblob_results['subjectivity']
    df_full['Polarity'] = textblob_results['polarity']

    # Apply Emotion Classification
    logging.info("Classifying emotion and tone categories...")
    df_full['Emotion_Tone'] = [
        classify_emotion_tone(row['Clean_Text'], row['Sentiment_Compound'])
        for _, row in df_full.iterrows()
    ]

    # Remove temporary clean_text column before saving
    df_export = df_full.drop(columns=['Clean_Text'])

    # 1. Export NEW Master Excel file (Do NOT overwrite original master file)
    master_nlp_output = "output/master/Reddit_Master_Scraped_Comments_NLP.xlsx"
    os.makedirs("output/master", exist_ok=True)
    os.makedirs("output/cases", exist_ok=True)

    with pd.ExcelWriter(master_nlp_output, engine='openpyxl') as writer:
        for case_name, df_case in df_export.groupby("Case"):
            sheet_title = str(case_name)[:31]
            df_case.to_excel(writer, index=False, sheet_name=sheet_title)

        # Build detailed NLP Summary tab
        summary_nlp = []
        for case_name, df_case in df_export.groupby("Case"):
            pos_pct = (df_case['Sentiment_Label'] == 'Positive').mean() * 100
            neu_pct = (df_case['Sentiment_Label'] == 'Neutral').mean() * 100
            neg_pct = (df_case['Sentiment_Label'] == 'Negative').mean() * 100
            avg_compound = df_case['Sentiment_Compound'].mean()
            
            summary_nlp.append({
                "Case": case_name,
                "Total Comments": len(df_case),
                "Avg Sentiment Score": round(avg_compound, 4),
                "% Positive": round(pos_pct, 2),
                "% Neutral": round(neu_pct, 2),
                "% Negative": round(neg_pct, 2),
                "Top Emotion": df_case['Emotion_Tone'].mode()[0] if not df_case.empty else "N/A"
            })
        df_sum_nlp = pd.DataFrame(summary_nlp)
        df_sum_nlp.to_excel(writer, index=False, sheet_name="NLP Summary")

    logging.info(f"Exported updated copy to NEW master file: {master_nlp_output}")

    # 2. Export updated Case Excel files
    for case_name, df_case in df_export.groupby("Case"):
        case_slug = str(case_name).replace(" ", "_")
        case_nlp_output = f"output/cases/{case_slug}_NLP.xlsx"
        with pd.ExcelWriter(case_nlp_output, engine='openpyxl') as writer:
            df_case.to_excel(writer, index=False, sheet_name=str(case_name))
        logging.info(f"Exported case file: {case_nlp_output}")

    # 3. Generate Analytical Visualizations
    generate_visualizations(df_export, output_dir="output/plots")

    # Log Topic Modeling Summary
    print("\n========================================================")
    print("TOPIC MODELING SUMMARY (LDA Key Themes per Brand)")
    print("========================================================")
    for case_name, df_case in df_export.groupby("Case"):
        topics = perform_topic_modeling(df_case, n_topics=3, n_words=5)
        print(f"\n--- Brand: {case_name} ---")
        for t in topics:
            print(f"  * {t}")

    print("\n========================================================")
    print("NLP ANALYSIS COMPLETE!")
    print(f"Updated Master File: {master_nlp_output}")
    print(f"Plots Saved in: output/plots/")
    print("========================================================\n")


if __name__ == "__main__":
    main()
