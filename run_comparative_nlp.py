"""
Comparative NLP Analysis Engine for Reddit Corporate Controversy Datasets
Runs VADER, TextBlob, Emotion Taxonomy, OHI, N-Grams, LDA Topic Modeling on:
1. Unfiltered Dataset (2,093 scraped comments, 1,617 valid text comments)
2. Filtered Dataset (1,302 comments)
3. Relevance Dataset (779 comments)

Generates updated Excel files, dataset-specific plots, comparative plots, and structured comparison tables.
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
        logging.FileHandler("nlp_comparative_analysis.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

vader_analyzer = SentimentIntensityAnalyzer()

CUSTOM_STOPWORDS = set(STOPWORDS).union({
    "reddit", "com", "https", "http", "www", "post", "comment", "people",
    "think", "know", "say", "said", "one", "even", "would", "could", "get",
    "got", "like", "make", "going", "see", "also", "much", "well"
})


def clean_text_for_nlp(text: str) -> str:
    """Cleans raw comment text by removing URLs, special characters, and extra spaces."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
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
    """Classifies comment tone into core emotion categories."""
    if not text:
        return "Skepticism / Neutral"
    
    text_lower = text.lower()
    
    betrayal_keywords = [
        "betray", "betrayed", "betrayal", "traitor", "traitors", "treason",
        "backstab", "backstabbed", "backstabbing", "backstabber", "sold out",
        "sellout", "turncoat", "stabbed in the back", "stab in the back",
        "double-cross", "switched sides", "unfaithful", "false promises"
    ]
    disappointment_keywords = [
        "disappoint", "disappointed", "disappointing", "disappointment",
        "letdown", "let down", "expected better", "shame", "shameful",
        "saddening", "unfortunate", "pity", "baffled", "baffling", "bummer",
        "disillusioned", "disheartening", "disheartened", "regret", "regrettable",
        "sadly", "underwhelmed", "lost respect", "unacceptable"
    ]
    anger_keywords = [
        "hate", "boycott", "boycotting", "boycotts", "outrage", "disgrace",
        "ridiculous", "idiot", "stupid", "garbage", "trash", "crap",
        "disgusting", "coward", "woke", "bigot", "fascist", "cancel", "scum",
        "infuriating", "pissed", "furious", "nauseating", "clowns", "bullshit"
    ]
    criticism_keywords = [
        "fail", "failed", "caved", "caving", "backtrack", "hypocrite", "hypocrisy",
        "ruined", "drop", "stop", "terrible", "awful", "pander", "pandering",
        "money", "greed", "mistake", "spineless", "clueless", "incompetent", "patronizing"
    ]
    fear_keywords = [
        "fear", "scared", "threat", "threatened", "threats", "violence", "danger",
        "warning", "afraid", "risk", "harm", "worry", "attack", "gun", "terror",
        "terrified", "terrifying", "unsafe", "hostile", "scary", "intimidate", "intimidation"
    ]
    support_keywords = [
        "support", "love", "great", "good", "respect", "agree", "based", "right",
        "smart", "thank", "thanks", "proud", "hero", "stand with", "awesome",
        "solid", "kudos", "props", "bravo", "fair", "sensible"
    ]

    has_betrayal = any(k in text_lower for k in betrayal_keywords)
    has_disappointment = any(k in text_lower for k in disappointment_keywords)
    has_anger = any(k in text_lower for k in anger_keywords)
    has_criticism = any(k in text_lower for k in criticism_keywords)
    has_fear = any(k in text_lower for k in fear_keywords)
    has_support = any(k in text_lower for k in support_keywords)

    if has_betrayal:
        return "Betrayal"
    elif has_disappointment:
        return "Disappointment"
    elif has_anger and compound_score < 0:
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


def compute_hostility_index(subjectivity: float, compound: float, neg: float) -> float:
    """Calculates Outrage & Hostility Index (0.0 to 1.0) per comment."""
    neg_intensity = max(0.0, -compound)
    score = (subjectivity * 0.4) + (neg_intensity * 0.4) + (neg * 0.2)
    return round(min(1.0, max(0.0, score)), 4)


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
    texts = [t for t in texts if len(t.strip()) > 5]
    if len(texts) < 5:
        return ["Insufficient text for topic modeling"]
    
    try:
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        tfidf = vectorizer.fit_transform(texts)
        
        lda = LatentDirichletAllocation(n_components=min(n_topics, len(texts)), random_state=42)
        lda.fit(tfidf)
        
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_features = [feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]]
            topics.append(f"Topic {topic_idx+1}: " + ", ".join(top_features))
        return topics
    except Exception as e:
        logging.warning(f"LDA Topic Modeling error: {e}")
        return [f"LDA Error: {e}"]


def load_and_process_dataset(file_path: str, dataset_label: str) -> pd.DataFrame:
    """Loads an excel dataset file, cleans comments, normalizes case names, and runs NLP pipeline."""
    logging.info(f"Processing dataset [{dataset_label}] from {file_path}...")
    xls = pd.ExcelFile(file_path)
    
    dfs = []
    for sheet in xls.sheet_names:
        if sheet in ["Summary", "NLP Summary", "TOTAL"]:
            continue
        df_sheet = pd.read_excel(xls, sheet_name=sheet)
        dfs.append(df_sheet)
        
    df_full = pd.concat(dfs, ignore_index=True)
    
    # Filter out empty/null comments
    df_full['Clean_Text'] = df_full['Comment Text'].apply(clean_text_for_nlp)
    df_full = df_full[df_full['Clean_Text'].str.len() > 2].copy()
    
    # Normalize Case names
    df_full['Case'] = df_full['Case'].replace({'Chicken-fil-A': 'Chick-fil-A', 'Chick-fil-a': 'Chick-fil-A'})
    
    # Recompute NLP metrics
    vader_results = df_full['Clean_Text'].apply(compute_vader_sentiment).apply(pd.Series)
    textblob_results = df_full['Clean_Text'].apply(compute_textblob_metrics).apply(pd.Series)

    df_full['Sentiment_Compound'] = vader_results['compound']
    df_full['Sentiment_Pos'] = vader_results['pos']
    df_full['Sentiment_Neu'] = vader_results['neu']
    df_full['Sentiment_Neg'] = vader_results['neg']
    df_full['Sentiment_Label'] = vader_results['label']
    df_full['Subjectivity'] = textblob_results['subjectivity']
    df_full['Polarity'] = textblob_results['polarity']

    df_full['Emotion_Tone'] = [
        classify_emotion_tone(row['Clean_Text'], row['Sentiment_Compound'])
        for _, row in df_full.iterrows()
    ]

    df_full['Hostility_Index'] = [
        compute_hostility_index(row['Subjectivity'], row['Sentiment_Compound'], row['Sentiment_Neg'])
        for _, row in df_full.iterrows()
    ]
    
    df_full['Dataset'] = dataset_label
    return df_full


def generate_dataset_plots(df: pd.DataFrame, output_dir: str, dataset_label: str):
    """Generates analytical charts for a specific dataset."""
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Generating charts for [{dataset_label}] in {output_dir}...")
    
    palette = {"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"}
    emotion_order = ["Anger / Outrage", "Betrayal", "Disappointment", "Disgust / Criticism", "Fear / Concern", "Support / Loyalty", "Skepticism / Neutral"]

    # 1. Sentiment Distribution by Case (%)
    plt.figure(figsize=(10, 6))
    sentiment_counts = pd.crosstab(df['Case'], df['Sentiment_Label'], normalize='index') * 100
    cols = [c for c in ['Positive', 'Neutral', 'Negative'] if c in sentiment_counts.columns]
    ax = sentiment_counts[cols].plot(
        kind='bar', stacked=True, color=[palette[c] for c in cols], figsize=(10, 6)
    )
    plt.title(f"[{dataset_label}] Sentiment Distribution by Case (%)", fontsize=14, fontweight='bold', pad=15)
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
    plt.savefig(f"{output_dir}/01_sentiment_distribution.png", dpi=300)
    plt.close()

    # 2. Emotion Distribution by Case
    plt.figure(figsize=(14, 6))
    sns.countplot(data=df, x='Emotion_Tone', hue='Case', order=emotion_order, palette='Set2')
    plt.title(f"[{dataset_label}] Emotion & Tone Distribution by Brand", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Emotion / Tone Category", fontsize=12)
    plt.ylabel("Comment Count", fontsize=12)
    plt.xticks(rotation=20, ha='right', fontsize=10)
    plt.legend(title="Brand Case")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_emotion_distribution.png", dpi=300)
    plt.close()

    # 3. Top Bigrams by Case
    cases = df['Case'].unique()
    fig, axes = plt.subplots(1, len(cases), figsize=(6 * len(cases), 6), sharey=False)
    if len(cases) == 1:
        axes = [axes]
    for idx, case in enumerate(cases):
        case_texts = df[df['Case'] == case]['Comment Text'].dropna().tolist()
        top_bigrams = extract_top_ngrams(case_texts, ngram_range=(2, 2), top_n=10)
        if top_bigrams:
            words, counts = zip(*top_bigrams)
            axes[idx].barh(list(words)[::-1], list(counts)[::-1], color='#3498db')
            axes[idx].set_title(f"Top Bigrams: {case}", fontsize=12, fontweight='bold')
            axes[idx].set_xlabel("Frequency", fontsize=10)
        else:
            axes[idx].text(0.5, 0.5, "No Bigrams Found", ha='center', va='center')
    plt.suptitle(f"[{dataset_label}] Top Keyphrase Bigrams per Brand", fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/03_top_bigrams.png", dpi=300)
    plt.close()

    # 4. Hostility Index Boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Emotion_Tone', y='Hostility_Index', hue='Emotion_Tone', order=emotion_order, palette='Reds', legend=False)
    plt.title(f"[{dataset_label}] Outrage & Hostility Index (OHI) by Emotion", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Emotion Category", fontsize=12)
    plt.ylabel("Hostility Index (0.0 to 1.0)", fontsize=12)
    plt.xticks(rotation=20, ha='right', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/04_hostility_index.png", dpi=300)
    plt.close()


def generate_comparison_plots(df_all: pd.DataFrame, output_dir: str):
    """Generates comparative visualizations across Unfiltered, Filtered, and Relevance datasets."""
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Generating comparative charts in {output_dir}...")
    
    ds_order = ["Unfiltered", "Filtered", "Relevance"]
    ds_colors = {"Unfiltered": "#95a5a6", "Filtered": "#3498db", "Relevance": "#e74c3c"}
    
    # 1. Total Comments by Dataset & Brand (Grouped Bar Chart)
    plt.figure(figsize=(10, 6))
    count_df = df_all.groupby(['Case', 'Dataset']).size().reset_index(name='Comment_Count')
    sns.barplot(data=count_df, x='Case', y='Comment_Count', hue='Dataset', hue_order=ds_order, palette=ds_colors)
    plt.title("Sample Size Reduction Across Datasets (Filtering & Auditing Impact)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Brand Case", fontsize=12)
    plt.ylabel("Number of Comments (n)", fontsize=12)
    for p in plt.gca().patches:
        height = p.get_height()
        if height > 0:
            plt.gca().annotate(f"{int(height)}", (p.get_x() + p.get_width() / 2., height + 10),
                               ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_comment_counts_comparison.png", dpi=300)
    plt.close()

    # 2. Negative Sentiment % Shift Across Datasets
    plt.figure(figsize=(11, 6))
    sentiment_pct = df_all.groupby(['Case', 'Dataset', 'Sentiment_Label']).size().unstack(fill_value=0)
    sentiment_pct = sentiment_pct.div(sentiment_pct.sum(axis=1), axis=0) * 100
    sentiment_pct = sentiment_pct.reset_index()
    
    sns.barplot(data=sentiment_pct, x='Case', y='Negative', hue='Dataset', hue_order=ds_order, palette=ds_colors)
    plt.title("Negative Sentiment Proportion (%) Across Datasets", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Brand Case", fontsize=12)
    plt.ylabel("Negative Comments (%)", fontsize=12)
    for p in plt.gca().patches:
        height = p.get_height()
        if height > 0:
            plt.gca().annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height + 1),
                               ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_negative_sentiment_shift.png", dpi=300)
    plt.close()

    # 3. Average Hostility Index (OHI) Shift Across Datasets
    plt.figure(figsize=(11, 6))
    hostility_df = df_all.groupby(['Case', 'Dataset'])['Hostility_Index'].mean().reset_index()
    sns.barplot(data=hostility_df, x='Case', y='Hostility_Index', hue='Dataset', hue_order=ds_order, palette=ds_colors)
    plt.title("Average Hostility & Outrage Index (OHI) Shift Across Datasets", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Brand Case", fontsize=12)
    plt.ylabel("Average Hostility Index (0.0 to 1.0)", fontsize=12)
    for p in plt.gca().patches:
        height = p.get_height()
        if height > 0:
            plt.gca().annotate(f"{height:.4f}", (p.get_x() + p.get_width() / 2., height + 0.01),
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/03_hostility_index_comparison.png", dpi=300)
    plt.close()

    # 4. Focal Outrage Emotions Comparison (Anger, Betrayal, Disappointment, Fear)
    focal_emotions = ["Anger / Outrage", "Betrayal", "Disappointment", "Fear / Concern"]
    df_focal = df_all[df_all['Emotion_Tone'].isin(focal_emotions)]
    
    plt.figure(figsize=(14, 7))
    emo_pct = df_all.groupby(['Dataset', 'Emotion_Tone']).size().unstack(fill_value=0)
    emo_pct = emo_pct.div(emo_pct.sum(axis=1), axis=0) * 100
    emo_pct = emo_pct[focal_emotions].reindex(ds_order).T
    
    emo_pct.plot(kind='bar', figsize=(12, 6), color=[ds_colors[d] for d in ds_order], width=0.8)
    plt.title("Focal Emotion Proportions (%) Across Full Corpus Datasets", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Emotion / Stance Category", fontsize=12)
    plt.ylabel("Proportion of Total Dataset Comments (%)", fontsize=12)
    plt.xticks(rotation=0, fontsize=11)
    for p in plt.gca().patches:
        height = p.get_height()
        if height > 0:
            plt.gca().annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height + 0.5),
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/04_focal_emotions_comparison.png", dpi=300)
    plt.close()


def main():
    logging.info("Starting Comparative NLP Analysis Engine...")
    
    file_paths = {
        "Unfiltered": "output/master/Reddit_Master_Scraped_Comments.xlsx",
        "Filtered": "output/Reddit_Master_Scraped_Comments_NLP_filtered.xlsx",
        "Relevance": "output/Reddit_Master_Scraped_Comments_NLP_Audited_Relevance.xlsx"
    }
    
    processed_dfs = {}
    summary_records = []
    lda_topics_records = []
    
    for label, path in file_paths.items():
        if not os.path.exists(path):
            logging.error(f"File not found for [{label}]: {path}")
            continue
        
        df_proc = load_and_process_dataset(path, label)
        processed_dfs[label] = df_proc
        
        # Save individual dataset plots
        plots_dir = f"output/plots_{label.lower()}"
        generate_dataset_plots(df_proc, plots_dir, label)
        
        # Export updated Excel file for each dataset
        out_excel = f"output/master/Reddit_Master_NLP_{label}.xlsx"
        os.makedirs("output/master", exist_ok=True)
        
        with pd.ExcelWriter(out_excel, engine='openpyxl') as writer:
            for case_name, df_case in df_proc.groupby("Case"):
                df_case.drop(columns=['Clean_Text']).to_excel(writer, index=False, sheet_name=str(case_name)[:31])
                
            # Build Dataset NLP Summary
            sum_rows = []
            for case_name, df_case in df_proc.groupby("Case"):
                n = len(df_case)
                pos = (df_case['Sentiment_Label'] == 'Positive').mean() * 100
                neu = (df_case['Sentiment_Label'] == 'Neutral').mean() * 100
                neg = (df_case['Sentiment_Label'] == 'Negative').mean() * 100
                
                anger = (df_case['Emotion_Tone'] == 'Anger / Outrage').mean() * 100
                betrayal = (df_case['Emotion_Tone'] == 'Betrayal').mean() * 100
                disappointment = (df_case['Emotion_Tone'] == 'Disappointment').mean() * 100
                fear = (df_case['Emotion_Tone'] == 'Fear / Concern').mean() * 100
                support = (df_case['Emotion_Tone'] == 'Support / Loyalty').mean() * 100
                skepticism = (df_case['Emotion_Tone'] == 'Skepticism / Neutral').mean() * 100
                
                avg_comp = df_case['Sentiment_Compound'].mean()
                avg_host = df_case['Hostility_Index'].mean()
                avg_up = df_case['Upvotes / Score'].mean()
                
                rec = {
                    "Dataset": label,
                    "Case": case_name,
                    "Total Comments (n)": n,
                    "Avg Sentiment Score": round(avg_comp, 4),
                    "Avg Hostility Index (OHI)": round(avg_host, 4),
                    "Avg Upvotes": round(avg_up, 2),
                    "% Negative": round(neg, 2),
                    "% Neutral": round(neu, 2),
                    "% Positive": round(pos, 2),
                    "% Anger / Outrage": round(anger, 2),
                    "% Betrayal": round(betrayal, 2),
                    "% Disappointment": round(disappointment, 2),
                    "% Fear / Concern": round(fear, 2),
                    "% Support / Loyalty": round(support, 2),
                    "% Skepticism / Neutral": round(skepticism, 2),
                    "Dominant Emotion": df_case['Emotion_Tone'].mode()[0] if not df_case.empty else "N/A"
                }
                sum_rows.append(rec)
                summary_records.append(rec)
                
                # LDA Topic Modeling for this dataset & brand
                topics = perform_topic_modeling(df_case, n_topics=3, n_words=5)
                for t in topics:
                    lda_topics_records.append({
                        "Dataset": label,
                        "Case": case_name,
                        "LDA Topic": t
                    })
                    
            df_sum = pd.DataFrame(sum_rows)
            df_sum.to_excel(writer, index=False, sheet_name="NLP Summary")
            
        logging.info(f"Exported updated dataset file: {out_excel}")

    # Combine all datasets for comparison
    df_combined = pd.concat(list(processed_dfs.values()), ignore_index=True)
    
    # Generate comparative plots
    generate_comparison_plots(df_combined, "output/plots_comparison")
    
    # Save Master Comparison Excel File
    df_master_sum = pd.DataFrame(summary_records)
    df_lda_sum = pd.DataFrame(lda_topics_records)
    
    comparison_excel = "output/master/NLP_Dataset_Comparison.xlsx"
    with pd.ExcelWriter(comparison_excel, engine='openpyxl') as writer:
        df_master_sum.to_excel(writer, index=False, sheet_name="Overall Summary")
        for case_name in df_combined['Case'].unique():
            df_c = df_master_sum[df_master_sum['Case'] == case_name]
            df_c.to_excel(writer, index=False, sheet_name=str(case_name)[:31])
        df_lda_sum.to_excel(writer, index=False, sheet_name="LDA Topics Comparison")
        
    logging.info(f"Exported Master Comparison Excel: {comparison_excel}")
    print("\n========================================================")
    print("COMPARATIVE NLP ANALYSIS COMPLETE!")
    print(f"Master Comparison Excel: {comparison_excel}")
    print("Plots saved in: output/plots_unfiltered, output/plots_filtered, output/plots_relevance, output/plots_comparison")
    print("========================================================\n")


if __name__ == "__main__":
    main()
