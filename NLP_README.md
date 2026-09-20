# Reddit Controversy NLP & Sentiment Analysis Engine

This module provides a comprehensive Natural Language Processing (NLP) and sentiment analysis pipeline applied to the dataset of 2,093 Reddit comments regarding corporate controversy cases: **Chick-fil-A**, **Bud Light**, and **Target**.

---

## Technical Overview & Methodology

The analysis pipeline (`nlp_analysis.py`) performs the following analytical steps:

### 1. Data Preprocessing & Cleaning
- Strips URLs, markdown formatting, emojis, special characters, and extra white space.
- Normalizes text while preserving casing for sentiment engines sensitive to capitalization (e.g. VADER).

### 2. Sentiment Analysis
- **VADER Sentiment Analyzer**: Optimized for social media discourse. Calculates `Compound` score (-1.0 to +1.0), `Positive`, `Neutral`, and `Negative` proportions.
- **Categorical Classification**:
  - `Positive`: `Compound Score >= 0.05`
  - `Neutral`: `-0.05 < Compound Score < 0.05`
  - `Negative`: `Compound Score <= -0.05`
- **TextBlob Metrics**: Computes `Subjectivity` (0.0 = highly objective, 1.0 = highly subjective) and `Polarity`.

### 3. Emotion & Stance Rule Engine
Classifies comments into five core emotional tones based on keyword patterns and sentiment alignment:
- `Anger / Outrage`: Negative sentiment combined with hostility, boycott calls, or aggressive terms.
- `Disgust / Criticism`: Negative sentiment focusing on corporate policy failure, pandering, or greed.
- `Fear / Concern`: Concern over safety threats, violent backlash, or extremism.
- `Support / Loyalty`: Positive sentiment expressing brand alignment or agreement.
- `Skepticism / Neutral`: Factual discourse or unopinionated observations.

### 4. N-Gram & Keyphrase Mining
- Uses `scikit-learn` `CountVectorizer` to extract top unigrams, bigrams, and trigrams per brand.
- Filters out standard English and Reddit-specific stopwords.

### 5. Topic Modeling (LDA)
- Fits Latent Dirichlet Allocation (LDA) models on TF-IDF matrices to uncover 3 dominant thematic topics per controversy case.

---

## File Deliverables & Output Hierarchy

```
scrapping_reddit/
├── nlp_analysis.py          # Main NLP execution engine (Python)
├── NLP_README.md            # Technical documentation
├── NLP_Analysis_Report.md   # Executive research & findings report
└── output/
    ├── master/
    │   ├── Reddit_Master_Scraped_Comments.xlsx      # Original Master File (Preserved)
    │   └── Reddit_Master_Scraped_Comments_NLP.xlsx  # NEW Updated Master File with NLP Columns
    ├── cases/
    │   ├── Chick-fil-A_NLP.xlsx
    │   ├── Bud_Light_NLP.xlsx
    │   └── Target_NLP.xlsx
    └── plots/
        ├── 01_sentiment_distribution_by_case.png
        ├── 02_sentiment_by_subreddit.png
        ├── 03_emotion_distribution_by_case.png
        ├── 04_upvote_vs_sentiment.png
        ├── 05_top_ngrams_by_case.png
        └── 06_wordcloud_by_case.png
```

---

## Setup & Execution

### Dependencies Installed
- `vaderSentiment`
- `textblob`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `wordcloud`
- `pandas` & `openpyxl`

### Running the Analysis
To run or re-run the complete NLP pipeline:

```bash
python3 nlp_analysis.py
```
