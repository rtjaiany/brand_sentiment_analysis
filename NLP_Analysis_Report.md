# Executive NLP & Sentiment Analysis Report: Corporate Controversy Discourse on Reddit

**Dataset Scope**: 2,093 Reddit comments scraped across 28 posts covering three major brand controversy cases (**Chick-fil-A**, **Bud Light**, and **Target**).  
**Methodology**: VADER Sentiment Intensity Analysis, TextBlob Subjectivity Analysis, Keyword/N-Gram Mining, Rule-Based Emotion Classification, and Latent Dirichlet Allocation (LDA) Topic Modeling.

---

## Key Executive Insights

1. **Target Experienced the Highest Hostility & Polarization**:
    - Target displayed the lowest average sentiment compound score (**-0.1463**) and the highest proportion of negative comments (**42.29%**).
    - Unlike Chick-fil-A or Bud Light, Target discourse was heavily dominated by **Fear & Threat Concerns (20.89%)**, alongside **Disappointment (2.07%)** from LGBTQ+ allies feeling the brand caved to anti-pride pressure.

2. **Bud Light's Discourse is Divided & Anger-Driven**:
    - Bud Light generated the highest concentration of **Anger / Outrage (19.89%)**, with intense debates surrounding "caving to pressure", "woke marketing", and "boycotting beer".
    - However, it also retained a significant positive contingent (**37.10%**), primarily composed of users criticizing the boycott or mocking the outrage.

3. **Chick-fil-A Registered Highest Betrayal Sentiment**:
    - Chick-fil-A showed the highest concentration of **Betrayal (2.96%)** and **Disappointment (2.96%)**, driven by conservative consumers who felt "sold out" or "stabbed in the back" when the brand altered its charitable donation model.
    - Despite this, Chick-fil-A retained strong brand loyalty (**23.67% Support**).

4. **Distinct Analysis of Betrayal vs. Disappointment**:
    - **Betrayal**: Expresses feelings of betrayal, treason, or sellout by previously trusted brands (highest in Chick-fil-A at 2.96%).
    - **Disappointment**: Reflects sadness, letdown, or unmet expectations (highest volume in Target with 36 comments, 2.07%, and Chick-fil-A with 2.96%).

---

## Quantitative Sentiment & Emotion Comparison

| Brand Case      | Total Comments | Negative (%) | Neutral (%) | Positive (%) | Avg Compound | Top Emotion Tones                                              | Betrayal (%) | Disappointment (%) |
| :-------------- | :------------: | :----------: | :---------: | :----------: | :----------: | :------------------------------------------------------------- | :----------: | :----------------: |
| **Chick-fil-A** |      169       |    39.05%    |   28.99%    |    31.95%    |   -0.0102    | Skepticism (45.56%), Support (23.67%), Anger (15.38%)          |  **2.96%**   |     **2.96%**      |
| **Bud Light**   |      186       |    39.78%    |   23.12%    |    37.10%    |   -0.0110    | Skepticism (45.70%), Support (24.73%), Anger (19.89%)          |    0.00%     |       0.54%        |
| **Target**      |     1,738      |    42.29%    |   35.16%    |    22.55%    | **-0.1463**  | Skepticism (46.61%), **Fear/Concern (20.89%)**, Anger (16.92%) |    0.29%     |     **2.07%**      |

---

## Visualizations & Chart Artifacts

### 1. Overall Sentiment Distribution by Case

![Sentiment Distribution](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/01_sentiment_distribution_by_case.png)

_Figure 1: Comparison of Positive, Neutral, and Negative comment percentages across Chick-fil-A, Bud Light, and Target._

---

### 2. Subreddit Ideological Breakdown

![Sentiment by Subreddit](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/02_sentiment_by_subreddit.png)

_Figure 2: Sentiment polarity across major subreddits (r/news, r/Target, r/Conservative, r/lgbt, r/WhitePeopleTwitter)._

- `r/Conservative` comments focus on corporate policy changes, anti-woke criticism, and donation policy drops.
- `r/lgbt` and `r/WhitePeopleTwitter` comments focus on disappointment over corporate caving to extremist pressure and safety concerns for LGBTQ+ communities.

---

### 3. Emotional Tone Breakdown (Including Betrayal & Disappointment)

![Emotion Distribution](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/03_emotion_distribution_by_case.png)

_Figure 3: Breakdown of Anger/Outrage, Betrayal, Disappointment, Disgust/Criticism, Fear/Concern, and Support/Loyalty._

---

### 4. Top Keyphrase Bigrams per Brand

![Top N-Grams](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/05_top_ngrams_by_case.png)

_Figure 4: Most frequent 2-word keyphrases per brand controversy._

- **Chick-fil-A**: _"salvation army"_, _"fellowship christian"_, _"stop donating"_, _"fca salvation"_.
- **Bud Light**: _"bud light"_, _"anheuser busch"_, _"dylan mulvaney"_, _"stay in our lane"_.
- **Target**: _"pride merchandise"_, _"removing pride"_, _"extremists violence"_, _"target workers"_.

---

### 5. Controversy Word Clouds

![Word Clouds](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/06_wordcloud_by_case.png)

_Figure 5: Word frequency clouds highlights core narrative themes per brand._

---

## Exploratory Data Analysis (EDA) of Sentiments & Emotions

### 1. Virality & Community Engagement (Upvote Score by Emotion)

![Upvotes by Emotion](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/07_upvotes_by_emotion_boxplot.png)

_Figure 6: Upvote score distribution across emotion categories._

- **Fear & Threat Concerns drive the highest community upvoting** (Mean: **42.37 upvotes**), highlighting how safety concerns regarding employees and bomb threats resonated deeply across Reddit communities.
- **Anger / Outrage** ranks second in virality (Mean: **31.58 upvotes**), confirming that outrage content receives strong upvote momentum on platform feeds.
- **Disappointment** receives significant community support (Mean: **29.15 upvotes**), showing that expressions of dismay and letdown resonate with fellow users.
- **Skepticism / Neutral** comments receive significantly lower engagement (Mean: **11.52 upvotes**).

---

### 2. Subreddit Ideological Profile & Emotion Heatmap

![Subreddit Emotion Heatmap](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/08_emotion_by_subreddit_heatmap.png)

_Figure 7: Emotion tone percentage heatmap across top subreddits._

- **`r/WhitePeopleTwitter`**: Heavily skewed towards **Fear / Concern (33.04%)** and **Anger (18.26%)**, condemning violent anti-pride intimidation tactics.
- **`r/news`**: High concentration of **Fear / Concern (27.04%)** and lowest **Support (6.63%)**, focusing on corporate retreat and news reports.
- **`r/lgbt`**: Highest concentration of **Disappointment (5.37%)**, capturing heartbreak and dismay over corporations yielding to extremist boycotts.
- **`r/Target`**: Dominated by **Skepticism / Neutral (52.72%)** and **Support / Loyalty (16.10%)**, reflecting store employees discussing inventory and operational policies.

---

### 3. Subjectivity vs. Polarity Sentiment Quadrants
![Sentiment Quadrant](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/09_sentiment_subjectivity_quadrant.png)

*Figure 8: TextBlob Polarity vs. Subjectivity quadrant colored by emotion tone.*

- **Upper-Left Quadrant (High Subjectivity, Negative Polarity)**: Populated by **Anger / Outrage** and **Betrayal** comments, containing strong personal opinion words and accusatory rhetoric.

---

### 4. Temporal Emotion Progression (Anger, Betrayal & Disappointment Over Time)
![Temporal Progression](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/10_temporal_emotion_progression.png)

*Figure 9: Monthly volume progression of Anger, Betrayal, and Disappointment.*

- **Anger** spikes sharply during initial boycott announcements.
- **Betrayal** peaks when specific policy changes are formally announced (e.g. Chick-fil-A donation shifts).
- **Disappointment** persists longer as consumers react to long-term corporate responses.

---

### 5. Top Author Emotional Stances & Polarization Clusters
![Author Stances](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/11_author_polarization_clusters.png)

*Figure 10: Emotional stance breakdown for top active authors.*

---

### 6. Outrage & Hostility Index (OHI) Distribution Across Emotions
![Hostility Index](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/12_hostility_toxicity_index.png)

*Figure 11: Distribution of Outrage & Hostility Index (OHI) across emotions.*

- **Anger / Outrage** records the highest mean OHI (**0.527**).
- **Disappointment** records a high OHI (**0.490**).
- **Betrayal** records an OHI of **0.381**, demonstrating focused negative sentiment without extreme profane hostility.

---

## Topic Modeling Analysis (LDA Themes)

### Case 1: Chick-fil-A
1. **Topic 1 (Donation Shifts)**: `salvation army`, `christian athletes`, `stop donating`, `fellowship`
2. **Topic 2 (Food & Brand Loyalty)**: `chick fil a`, `best chicken`, `eat`, `food`
3. **Topic 3 (Political Reaction)**: `left pressure`, `lgbt`, `boycott`, `charity`

### Case 2: Bud Light
1. **Topic 1 (Marketing Controversy)**: `dylan mulvaney`, `anheuser busch`, `distancing`, `vp`
2. **Topic 2 (Boycott Impact)**: `sales drop`, `stay in lane`, `beer`, `drink`
3. **Topic 3 (Public Backlash)**: `woke`, `customers`, `apology`, `statement`

### Case 3: Target
1. **Topic 1 (Safety & Extremism)**: `terrorists`, `threats`, `violence`, `employees`, `safety`
2. **Topic 2 (Pride Collection)**: `pride merch`, `removing items`, `abprallen`, `displays`
3. **Topic 3 (Corporate Strategy)**: `caving`, `bigots`, `boycott`, `cpac`

---

## Output Data File Summary

- **Updated Master Excel**: [`output/master/Reddit_Master_Scraped_Comments_NLP.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/Reddit_Master_Scraped_Comments_NLP.xlsx)
  - Contains all original columns + 8 NLP columns (`Sentiment_Compound`, `Sentiment_Pos`, `Sentiment_Neu`, `Sentiment_Neg`, `Sentiment_Label`, `Subjectivity`, `Polarity`, `Emotion_Tone`, `Hostility_Index`).
- **Original Master File**: [`output/master/Reddit_Master_Scraped_Comments.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/Reddit_Master_Scraped_Comments.xlsx) *(Unmodified)*.
- **Plot Directory**: [`output/plots/`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/) (Contains all 12 generated high-resolution PNG charts).
