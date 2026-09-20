# Executive NLP & Sentiment Analysis Report: Corporate Controversy Discourse on Reddit

**Dataset Scope**: 2,093 Reddit comments scraped across 28 posts covering three major brand controversy cases (**Chick-fil-A**, **Bud Light**, and **Target**).  
**Methodology**: VADER Sentiment Intensity Analysis, TextBlob Subjectivity Analysis, Keyword/N-Gram Mining, Rule-Based Emotion Classification, and Latent Dirichlet Allocation (LDA) Topic Modeling.

---

## Key Executive Insights

1. **Target Experienced the Highest Hostility & Polarization**:
   - Target displayed the lowest average sentiment compound score (**-0.1463**) and the highest proportion of negative comments (**42.29%**).
   - Unlike Chick-fil-A or Bud Light, Target discourse was heavily dominated by **Fear & Threat Concerns (21.46%)**, driven by news regarding violence/threats against store employees and extremist boycott tactics.

2. **Bud Light's Discourse is Divided & Anger-Driven**:
   - Bud Light generated the highest concentration of **Anger / Outrage (20.43%)**, with intense debates surrounding "caving to pressure", "woke marketing", and "boycotting beer".
   - However, it also retained a significant positive contingent (**37.10%**), primarily composed of users criticizing the boycott or mocking the outrage.

3. **Chick-fil-A Retained Stronger Core Brand Support**:
   - Despite initial conservative backlash over dropping donations to the Salvation Army & FCA, Chick-fil-A retained the highest proportion of **Support & Loyalty (24.85%)** among the three cases.

---

## Quantitative Sentiment Comparison

| Brand Case | Total Comments | Negative (%) | Neutral (%) | Positive (%) | Avg Compound Score | Primary Emotion Tone |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Chick-fil-A** | 169 | 39.05% | 28.99% | 31.95% | -0.0102 | Skepticism (45.56%), Support (24.85%) |
| **Bud Light** | 186 | 39.78% | 23.12% | 37.10% | -0.0110 | Skepticism (45.70%), Support (24.73%), Anger (20.43%) |
| **Target** | 1,738 | 42.29% | 35.16% | 22.55% | **-0.1463** | Skepticism (47.07%), **Fear/Concern (21.46%)** |

---

## Visualizations & Chart Artifacts

### 1. Overall Sentiment Distribution by Case
![Sentiment Distribution](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/01_sentiment_distribution_by_case.png)

*Figure 1: Comparison of Positive, Neutral, and Negative comment percentages across Chick-fil-A, Bud Light, and Target.*

---

### 2. Subreddit Ideological Breakdown
![Sentiment by Subreddit](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/02_sentiment_by_subreddit.png)

*Figure 2: Sentiment polarity across major subreddits (r/news, r/Target, r/Conservative, r/lgbt, r/WhitePeopleTwitter).*

- `r/Conservative` comments focus on corporate policy changes, anti-woke criticism, and donation policy drops.
- `r/lgbt` and `r/WhitePeopleTwitter` comments focus on disappointment over corporate caving to extremist pressure and safety concerns for LGBTQ+ communities.

---

### 3. Emotional Tone Breakdown
![Emotion Distribution](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/03_emotion_distribution_by_case.png)

*Figure 3: Breakdown of Anger/Outrage, Disgust/Criticism, Fear/Concern, and Support/Loyalty.*

---

### 4. Top Keyphrase Bigrams per Brand
![Top N-Grams](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/05_top_ngrams_by_case.png)

*Figure 4: Most frequent 2-word keyphrases per brand controversy.*

- **Chick-fil-A**: *"salvation army"*, *"fellowship christian"*, *"stop donating"*, *"fca salvation"*.
- **Bud Light**: *"bud light"*, *"anheuser busch"*, *"dylan mulvaney"*, *"stay in our lane"*.
- **Target**: *"pride merchandise"*, *"removing pride"*, *"extremists violence"*, *"target workers"*.

---

### 5. Controversy Word Clouds
![Word Clouds](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/06_wordcloud_by_case.png)

*Figure 5: Word frequency clouds highlights core narrative themes per brand.*

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
  - Contains all 17 original columns + 7 new NLP columns (`Sentiment_Compound`, `Sentiment_Pos`, `Sentiment_Neu`, `Sentiment_Neg`, `Sentiment_Label`, `Subjectivity`, `Emotion_Tone`).
- **Original Master File**: [`output/master/Reddit_Master_Scraped_Comments.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/Reddit_Master_Scraped_Comments.xlsx) *(Unmodified)*.
- **Plot Directory**: [`output/plots/`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/)
