# Reddit Controversy NLP & Sentiment Analysis Engine

This repository module provides an advanced Natural Language Processing (NLP) and sentiment analysis pipeline applied to **2,093 Reddit comments** across 28 posts covering three major corporate controversy cases: **Chick-fil-A**, **Bud Light**, and **Target**.

---

## Technical Overview & Detailed Methodology

The execution script [`nlp_analysis.py`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/nlp_analysis.py) implements a multi-stage analytical architecture combining lexicon-based sentiment engines, rule-based emotion taxonomy, composite outrage scoring, keyphrase frequency extraction, LDA topic modeling, and statistical Exploratory Data Analysis (EDA).

```
 Raw Reddit Data (Excel)
           │
           ▼
 1. Text Preprocessing & Cleaning
           │
           ▼
 2. Dual Sentiment Engines (VADER + TextBlob)
           │
           ▼
 3. Rule-Based 7-Class Emotion Engine (Focus: Anger, Betrayal, Disappointment)
           │
           ▼
 4. Outrage & Hostility Indexing (OHI Score)
           │
           ▼
 5. Keyphrase Mining (N-Grams) & Topic Modeling (LDA)
           │
           ▼
 6. Exploratory Data Analysis (12 Plots) & Excel Master Export
```

---

### Step 1: Text Preprocessing & Data Cleaning

Raw Reddit comments often contain noise, markdown syntax, embedded URLs, and formatting artifacts. The `clean_text_for_nlp` function standardizes raw text:
- **URL Removal**: Strips `http://`, `https://`, and `www.` links using regex `https?://\S+|www\.\S+`.
- **Markdown Link Cleaning**: Replaces `[anchor text](url)` with `anchor text` using regex `\[([^\]]+)\]\([^)]+\)`.
- **Whitespace Normalization**: Collapses multiple line breaks and spaces into a single space `\s+` -> `' '`.
- **Casing Preservation**: Preserves original capitalization during VADER calculation (as VADER leverages uppercase text like `"BOYCOTT"` for intensity boosting), while lowercasing text during keyword extraction.

---

### Step 2: Dual Sentiment Analysis Architecture

To ensure multi-dimensional evaluation, comments are analyzed using two complementary sentiment engines:

#### A. VADER (Valence Aware Dictionary and sEntiment Reasoner)
VADER is specifically calibrated for social media discourse, accounting for punctuation, capitalization, and contextual modifiers.
- **Metrics Calculated**:
  - `Sentiment_Pos`: Proportion of positive lexical tokens.
  - `Sentiment_Neu`: Proportion of neutral lexical tokens.
  - `Sentiment_Neg`: Proportion of negative lexical tokens.
  - `Sentiment_Compound`: Normalized score from `-1.0` (extreme negative) to `+1.0` (extreme positive).
- **Categorical Sentiment Thresholds**:
  - **Positive**: $\text{Compound} \ge +0.05$
  - **Neutral**: $-0.05 < \text{Compound} < +0.05$
  - **Negative**: $\text{Compound} \le -0.05$

#### B. TextBlob Sentiment & Subjectivity Analyzer
TextBlob provides additional linguistic metrics:
- `Polarity`: Measures lexical positivity/negativity on a scale from `-1.0` to `+1.0`.
- `Subjectivity`: Quantifies opinion vs. factual content on a scale from `0.0` (completely objective/factual) to `1.0` (highly subjective/opinionated).

---

### Step 3: Rule-Based 7-Class Emotion & Stance Taxonomy

Comments are categorized into **seven distinct emotional tones**, with a primary analytical focus on **Anger / Outrage**, **Betrayal**, and **Disappointment**:

1. **`Betrayal`**:
   - **Definition**: Expressions of feeling backstabbed, sold out, or deceived by a previously trusted brand.
   - **Keywords**: `betray`, `betrayed`, `betrayal`, `traitor`, `traitors`, `treason`, `backstab`, `backstabbed`, `backstabbing`, `backstabber`, `sold out`, `sellout`, `turncoat`, `stabbed in the back`, `stab in the back`, `double-cross`, `switched sides`, `unfaithful`, `false promises`.
2. **`Disappointment`**:
   - **Definition**: Expressions of sadness, letdown, lost respect, or unmet corporate expectations.
   - **Keywords**: `disappoint`, `disappointed`, `disappointing`, `disappointment`, `letdown`, `let down`, `expected better`, `shame`, `shameful`, `saddening`, `unfortunate`, `pity`, `baffled`, `baffling`, `bummer`, `disillusioned`, `disheartening`, `disheartened`, `regret`, `regrettable`, `sadly`, `underwhelmed`, `lost respect`, `unacceptable`.
3. **`Anger / Outrage`**:
   - **Definition**: Explicit hostility, boycott calls, aggressive insults, or high negative compound sentiment ($\le -0.50$).
   - **Keywords**: `hate`, `boycott`, `boycotting`, `boycotts`, `outrage`, `disgrace`, `ridiculous`, `idiot`, `stupid`, `garbage`, `trash`, `crap`, `disgusting`, `coward`, `woke`, `bigot`, `fascist`, `cancel`, `scum`, `infuriating`, `pissed`, `furious`, `nauseating`, `clowns`, `bullshit`.
4. **`Disgust / Criticism`**:
   - **Definition**: Negative sentiment focusing on corporate policy failure, pandering, greed, or incompetence.
   - **Keywords**: `fail`, `failed`, `caved`, `caving`, `backtrack`, `hypocrite`, `hypocrisy`, `ruined`, `drop`, `stop`, `terrible`, `awful`, `pander`, `pandering`, `money`, `greed`, `mistake`, `spineless`, `clueless`, `incompetent`, `patronizing`.
5. **`Fear / Concern`**:
   - **Definition**: Safety concerns regarding violent threats, employee harassment, or bomb threats.
   - **Keywords**: `fear`, `scared`, `threat`, `threatened`, `threats`, `violence`, `danger`, `warning`, `afraid`, `risk`, `harm`, `worry`, `attack`, `gun`, `terror`, `terrified`, `terrifying`, `unsafe`, `hostile`, `scary`, `intimidate`, `intimidation`.
6. **`Support / Loyalty`**:
   - **Definition**: Positive sentiment expressing brand alignment, defense, or high positive compound sentiment ($\ge +0.50$).
   - **Keywords**: `support`, `love`, `great`, `good`, `respect`, `agree`, `based`, `right`, `smart`, `thank`, `thanks`, `proud`, `hero`, `stand with`, `awesome`, `solid`, `kudos`, `props`, `bravo`, `fair`, `sensible`.
7. **`Skepticism / Neutral`**:
   - **Definition**: Factual discourse, news descriptions, or unopinionated observations.

---

### Step 4: Outrage & Hostility Index (OHI) Derivation

To quantify hostility intensity per comment on a normalized continuous scale (`0.0` to `1.0`), we derived the **Outrage & Hostility Index (OHI)**:

$$\text{OHI} = \min\left(1.0, \max\left(0.0, (\text{Subjectivity} \times 0.4) + (\max(0, -\text{Compound}) \times 0.4) + (\text{Sentiment\_Neg} \times 0.2)\right)\right)$$

#### Rationale:
- **Subjectivity Weight ($0.4$)**: Captures personal emotional opinion vs objective news posting.
- **Negative Compound Weight ($0.4$)**: Measures overall sentiment negativity severity.
- **Negative Token Weight ($0.2$)**: Measures lexical density of hostile/negative words.

---

### Step 5: N-Gram Keyphrase Extraction & Topic Modeling (LDA)

- **N-Gram Keyphrase Extraction**: `scikit-learn` `CountVectorizer` configured with `ngram_range=(2,2)` and `min_df=2` extracts top 2-word keyphrases per brand case after filtering standard English and Reddit custom stopwords (`CUSTOM_STOPWORDS`).
- **LDA Topic Modeling**: `TfidfVectorizer(max_features=1000)` combined with `LatentDirichletAllocation(n_components=3, random_state=42)` uncovers 3 dominant thematic topics per controversy case.

---

### Step 6: Visualizations & Output Hierarchy

The script generates **12 high-resolution analytical plots** in `output/plots/`:

```
scrapping_reddit/
├── nlp_analysis.py          # Main execution engine
├── NLP_README.md            # Technical methodology documentation
├── NLP_Analysis_Report.md   # Executive research report
└── output/
    ├── master/
    │   ├── Reddit_Master_Scraped_Comments.xlsx      # Original Master Workbook
    │   └── Reddit_Master_Scraped_Comments_NLP.xlsx  # Updated Master Workbook with NLP & OHI columns
    ├── cases/
    │   ├── Chick-fil-A_NLP.xlsx
    │   ├── Bud_Light_NLP.xlsx
    │   └── Target_NLP.xlsx
    └── plots/
        ├── 01_sentiment_distribution_by_case.png      # Stacked Bar: Positive/Neutral/Negative %
        ├── 02_sentiment_by_subreddit.png              # Grouped Bar: Top Subreddits by Sentiment
        ├── 03_emotion_distribution_by_case.png        # Grouped Bar: 7 Emotion Tones per Brand Case
        ├── 04_upvote_vs_sentiment.png                # Boxplot: Upvotes by Sentiment Category
        ├── 05_top_ngrams_by_case.png                 # Horizontal Bar: Top 2-Gram Keyphrases
        ├── 06_wordcloud_by_case.png                  # Word Clouds: Core narrative terms per Brand
        ├── 07_upvotes_by_emotion_boxplot.png         # Boxplot: Virality (Upvotes) by Emotion Category
        ├── 08_emotion_by_subreddit_heatmap.png       # Heatmap: Subreddit Ideology % per Emotion
        ├── 09_sentiment_subjectivity_quadrant.png    # Scatter Plot: Polarity vs Subjectivity Quadrants
        ├── 10_temporal_emotion_progression.png       # Line Plot: Timeline of Anger, Betrayal & Disappointment
        ├── 11_author_polarization_clusters.png       # Bar Chart: Top Author Emotional Stances
        └── 12_hostility_toxicity_index.png           # Boxplot: Outrage & Hostility Index (OHI)
```

---

## Setup & Execution

### Dependencies
- `vaderSentiment`, `textblob`, `scikit-learn`, `matplotlib`, `seaborn`, `wordcloud`, `pandas`, `openpyxl`, `scipy`

### Running the Analysis
To execute the complete NLP pipeline and regenerate all master Excel files, case workbooks, and 12 plots:

```bash
python3 nlp_analysis.py
```
