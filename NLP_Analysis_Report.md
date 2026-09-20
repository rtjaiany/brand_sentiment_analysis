# Executive NLP & Sentiment Analysis Report: Corporate Controversy Discourse on Reddit

**Dataset Scope**: 2,093 Reddit comments scraped across 28 posts covering three major corporate controversy cases: **Chick-fil-A** ($n=169$), **Bud Light** ($n=186$), and **Target** ($n=1,738$).  
**Methodology**: VADER Sentiment Intensity Analysis, TextBlob Subjectivity Analysis, N-Gram Keyphrase Frequency Mining, Rule-Based 7-Class Emotion Taxonomy, Outrage & Hostility Indexing (OHI), and Latent Dirichlet Allocation (LDA) Topic Modeling.

---

## Executive Summary & Focal Insights

This investigation examines public reaction to high-profile corporate controversies on Reddit. The analysis focuses primarily on three core negative emotional stances: **Anger / Outrage**, **Betrayal**, and **Disappointment**.

### Primary Findings:

1. **Target Experienced Severe Threat-Driven Hostility**:
   - Target accumulated the lowest average compound sentiment score (**-0.1463**) and the highest proportion of negative comments (**42.29%**).
   - Discourse was heavily dominated by **Fear & Safety Concerns (20.89%)** due to bomb threats and violence directed at store workers, paired with **Disappointment (2.42%)** from LGBTQ+ supporters.

2. **Bud Light Exhibited Polarized Ideological Outrage**:
   - Bud Light generated the highest percentage of **Anger / Outrage (20.97%)**, driven by conservative boycott calls.
   - Concurrently, it retained a substantial positive contingent (**37.10% Positive**), composed of users mocking the boycott or supporting Dylan Mulvaney.

3. **Chick-fil-A Recorded the Highest Concentration of Betrayal**:
   - Chick-fil-A registered the highest relative concentration of **Betrayal (2.96%)** and **Disappointment (2.96%)**.
   - Conservative loyalists expressed feeling "sold out" or "stabbed in the back" when the brand altered its charitable donation framework.

4. **Community Virality & Engagement Dynamics**:
   - **Fear & Threat Concerns** achieved the highest average upvote score (**42.37 upvotes**).
   - **Anger / Outrage** ranked second in community virality (**31.58 average upvotes**).
   - **Disappointment** generated strong community endorsement (**29.15 average upvotes**).
   - **Betrayal** averaged **4.50 upvotes**, occurring within specific niche subreddits (`r/atlanticdiscussions`, `r/Target`, `r/news`).

---

## Quantitative Sentiment & Emotion Comparison Table

| Brand Case | Comments ($n$) | Negative (%) | Neutral (%) | Positive (%) | Avg Compound | Avg Hostility (OHI) | Anger (%) | Betrayal (%) | Disappointment (%) | Fear (%) | Support (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Chick-fil-A** | 169 | 39.05% | 28.99% | 31.95% | -0.0102 | 0.3210 | 15.98% | **2.96%** | **2.96%** | 4.73% | 23.67% |
| **Bud Light** | 186 | 39.78% | 23.12% | 37.10% | -0.0110 | 0.3450 | **20.97%** | 0.00% | 0.54% | 4.84% | 24.73% |
| **Target** | 1,738 | 42.29% | 35.16% | 22.55% | **-0.1463** | **0.3890** | 17.09% | 0.29% | **2.42%** | **20.89%** | 11.57% |

---

## Comprehensive Analytical Breakdown by Visualizations

---

### Section 1: Brand Sentiment & Subreddit Ideology

#### Figure 1: Overall Sentiment Distribution by Controversy Case
![Sentiment Distribution](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/01_sentiment_distribution_by_case.png)

*Figure 1: Comparison of Positive, Neutral, and Negative comment proportions across Chick-fil-A, Bud Light, and Target.*

**Results & Insights**:
- **Target** displays the highest percentage of negative sentiment (**42.3%**), reflecting widespread criticism of corporate caving and security concerns.
- **Bud Light** shows a bimodal split with **37.1% Positive** and **39.8% Negative**, representing intense polarization between boycotters and anti-boycott commenters.
- **Chick-fil-A** exhibits a balanced distribution (**39.1% Negative, 32.0% Positive, 29.0% Neutral**), reflecting persistent brand defense among core customers despite donation policy shifts.

---

#### Figure 2: Sentiment Polarity Breakdown Across Top Subreddits
![Sentiment by Subreddit](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/02_sentiment_by_subreddit.png)

*Figure 2: Sentiment breakdown across major subreddits (r/news, r/Target, r/Conservative, r/lgbt, r/WhitePeopleTwitter).*

**Results & Insights**:
- `r/Conservative`: Dominated by **Negative sentiment** focused on corporate wokeism and donation policy changes.
- `r/WhitePeopleTwitter` & `r/news`: High volume of negative comments condemning anti-pride threats and corporate retreat.
- `r/Target`: Dominated by **Neutral sentiment** from retail employees discussing operational impacts.

---

### Section 2: Emotion Taxonomy & Keyphrase Analysis

#### Figure 3: Emotion & Tone Distribution by Brand Controversy
![Emotion Distribution](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/03_emotion_distribution_by_case.png)

*Figure 3: Breakdown of Anger/Outrage, Betrayal, Disappointment, Disgust/Criticism, Fear/Concern, and Support/Loyalty.*

**Results & Insights**:
- **Anger / Outrage**: Reaches its highest proportion in **Bud Light (20.97%)** and **Target (17.09%)**.
- **Betrayal**: Concentrated primarily in **Chick-fil-A (2.96%)**, where core conservative supporters felt abandoned after donation policy modifications.
- **Disappointment**: Highest in **Chick-fil-A (2.96%)** and **Target (2.42%)**, expressing sadness over corporate capitulation.
- **Fear / Concern**: Dominates **Target (20.89%)**, driven by store safety and bomb threat reports.

---

#### Figure 4: Most Frequent Keyphrase Bigrams per Brand Case
![Top N-Grams](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/05_top_ngrams_by_case.png)

*Figure 4: Top 2-word keyphrase bigrams extracted per brand controversy.*

**Results & Insights**:
- **Chick-fil-A**: Dominant bigrams include *"salvation army"*, *"fellowship christian"*, *"stop donating"*, and *"christian athletes"*.
- **Bud Light**: Dominant bigrams include *"bud light"*, *"anheuser busch"*, *"dylan mulvaney"*, and *"stay lane"*.
- **Target**: Dominant bigrams include *"pride merchandise"*, *"removing pride"*, *"extremists violence"*, and *"target workers"*.

---

#### Figure 5: Word Clouds of Comment Text per Brand Controversy
![Word Clouds](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/06_wordcloud_by_case.png)

*Figure 5: Word frequency clouds highlighting core narrative themes per brand.*

**Results & Insights**:
- Visualizes prominent narrative terms per brand: **Bud Light** centers on marketing leadership and boycott efficacy; **Chick-fil-A** centers on religious charities; **Target** centers on employee safety and pride displays.

---

### Section 3: Engagement, Heatmaps & Sentiment Quadrants (EDA)

#### Figure 6: Upvote Engagement & Virality Across Emotion Categories
![Upvotes by Emotion](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/07_upvotes_by_emotion_boxplot.png)

*Figure 6: Upvote score distribution across emotion categories.*

**Results & Insights**:
- **Fear & Threat Concerns**: Highest mean upvote score (**42.37 upvotes**), reflecting broad community resonance around worker safety.
- **Anger / Outrage**: Second highest virality (**31.58 average upvotes**), confirming that outrage drives platform engagement.
- **Disappointment**: High community agreement (**29.15 average upvotes**).
- **Betrayal**: Averages **4.50 upvotes**, occurring in specific niche subreddits (`r/atlanticdiscussions`, `r/Target`, `r/news`, `r/TraditionalCatholics`).

---

#### Figure 7: Subreddit Ideological Emotion Heatmap (%)
![Subreddit Emotion Heatmap](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/08_emotion_by_subreddit_heatmap.png)

*Figure 7: Heatmap of emotion category percentages across top subreddits.*

**Results & Insights**:
- **`r/WhitePeopleTwitter`**: High **Fear / Concern (33.04%)** and **Anger (18.26%)**.
- **`r/lgbt`**: Highest concentration of **Disappointment (5.37%)**.
- **`r/news`**: High **Fear / Concern (27.04%)** and lowest **Support (6.63%)**.
- **`r/Target`**: High **Skepticism / Neutral (52.72%)** and **Support / Loyalty (16.10%)**.

---

#### Figure 8: TextBlob Polarity vs. Subjectivity Quadrant Mapping
![Sentiment Quadrant](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/09_sentiment_subjectivity_quadrant.png)

*Figure 8: Scatter plot mapping comment Subjectivity vs Polarity colored by emotion tone.*

**Results & Insights**:
- **Upper-Left Quadrant (High Subjectivity $\ge 0.5$, Negative Polarity $< 0.0$)**: Populated almost exclusively by **Anger / Outrage** and **Betrayal**, containing high opinion intensity and accusatory language.
- **Lower-Middle Quadrant (Low Subjectivity $< 0.5$, Neutral Polarity $\approx 0.0$)**: Populated by news reporting, factual observations, and **Skepticism / Neutral** comments.

---

### Section 4: Temporal Progression, Author Stances & Hostility Index

#### Figure 9: Temporal Progression of Primary Outrage Emotions
![Temporal Progression](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/10_temporal_emotion_progression.png)

*Figure 9: Monthly volume progression of Anger, Betrayal, and Disappointment.*

**Results & Insights**:
- **Anger / Outrage** exhibits immediate spikes during initial news breaks and boycott calls.
- **Betrayal** peaks when specific policy modifications are officially confirmed.
- **Disappointment** maintains a longer tail, reflecting sustained letdown as consumers evaluate corporate responses over time.

---

#### Figure 10: Top Active Author Stances & Polarization Clusters
![Author Stances](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/11_author_polarization_clusters.png)

*Figure 10: Emotional stance breakdown for top active authors.*

**Results & Insights**:
- Evaluates author engagement personas: Top active commenters demonstrate consistent emotional stances, categorizing users into *Outrage Detractors*, *Disappointed Allies*, and *Neutral Observers*.

---

#### Figure 11: Outrage & Hostility Index (OHI) Distribution Across Emotions
![Hostility Index](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/12_hostility_toxicity_index.png)

*Figure 11: Distribution of Outrage & Hostility Index (OHI) across emotion categories.*

**Results & Insights**:
- **Anger / Outrage** records the highest average OHI score (**0.527**).
- **Disappointment** records a high OHI score (**0.490**).
- **Betrayal** records an OHI score of **0.381**, demonstrating focused negative sentiment without extreme profane hostility.

---

#### Figure 12: Upvote Score Distribution by Sentiment Polarity Label
![Upvote vs Sentiment](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots/04_upvote_vs_sentiment.png)

*Figure 12: Boxplot distribution of upvotes across Positive, Neutral, and Negative sentiment labels.*

**Results & Insights**:
- Negative sentiment comments consistently show higher upvote dispersion and higher upper quartiles compared to neutral comments.

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
