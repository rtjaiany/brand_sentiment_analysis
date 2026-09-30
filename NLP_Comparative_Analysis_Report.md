# Relatório Comparativo de Análise de Sentimento & NLP: Controvérsias Corporativas no Reddit

**Escopo da Comparação**: Análise comparativa entre 3 níveis de tratamento da base de dados de comentários do Reddit sobre controvérsias corporativas (**Chick-fil-A**, **Bud Light** e **Target**):
1. **Base Não Filtrada (Unfiltered / Original)**: $n = 1.611$ comentários válidos ($2.093$ linhas totais raspadas).
2. **Base Filtrada (Filtered)**: $n = 1.301$ comentários selecionados (remoção de comentários off-topic e ruídos gerais).
3. **Base Auditada de Relevância (Audited Relevance)**: $n = 779$ comentários altamente específicos e diretamente alinhados ao fenômeno de interesse.

---

## 1. Resumo Executivo & Principais Descobertas

O processo de filtragem e auditoria de relevância demonstrou um impacto quantitativo e qualitativo significativo na precisão dos indicadores de NLP, revelando padrões mais nítidos sobre as reações do público em relação ao fenômeno de controvérsia corporativa:

### 1. Amplificação da Intensidade Negativa e Redução de Ruído
* **Target**: O percentual de comentários negativos subiu de **56,93%** na base não filtrada para **59,71%** na base de relevância auditada, enquanto o tom médio de sentimento (*VADER Compound*) caiu de **-0.1972** para **-0.2172**. 
* **Bud Light**: A negatividade aumentou de **43,53%** para **47,50%**, enquanto o Índice de Hostilidade e Ultraje (*Outrage & Hostility Index - OHI*) cresceu de **0,2918** para **0,3489** (+19,6% de concentração de hostilidade).
* **Chick-fil-A**: A proporção de sentimento negativo cresceu de **43,33%** para **50,00%**, e a categoria de **Decepção / Disappointment** dobrou de **3,33%** para **7,41%**.

### 2. Revelação de Sentimentos Ocultos
Na base não filtrada de **Chick-fil-A**, comentários irrelevantes sobre preferência alimentar ("o Popeyes é melhor", "gosto das batatas waffle") diluíam as reações de decepção e traição ideológica. Na base auditada de relevância, a **Decepção (7,41%)** e a **Traição / Betrayal (3,70%)** atingiram suas maiores concentrações em relação a todas as marcas.

### 3. Concentração do Fator "Medo & Violência" na Target
À medida que a base foi refinada para comentários estritamente relevantes, a categoria de **Medo / Preocupação com Segurança (Fear / Concern)** na Target disparou de **28,12%** na base não filtrada para **34,60%** na base de relevância. Isso confirma que os comentários mais relevantes em relação ao fenômeno da Target focavam nas ameaças de bomba, segurança dos trabalhadores e recuo corporativo.

---

## 2. Tabela Quantitativa Comparativa Completa

A tabela abaixo apresenta a comparação detalhada dos indicadores quantitativos de NLP entre as três bases:

| Base / Tratamento | Marca / Case | Amostra Válida ($n$) | Negativo (%) | Neutro (%) | Positivo (%) | Sentimento Médio (Compound) | Índice Hostilidade (OHI) | Raiva / Outrage (%) | Traição / Betrayal (%) | Decepção / Disappointment (%) | Medo / Fear (%) | Suporte / Loyalty (%) | Escepticismo / Neutral (%) | Emoção Dominante |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Unfiltered** | **Bud Light** | 170 | 43.53% | 15.88% | 40.59% | -0.0120 | 0.2918 | 22.94% | 0.00% | 0.59% | 5.29% | 27.06% | 40.00% | Skepticism / Neutral |
| **Filtered** | **Bud Light** | 94 | 46.81% | 13.83% | 39.36% | -0.0763 | 0.3219 | **27.66%** | 0.00% | 0.00% | 4.26% | 23.40% | 38.30% | Skepticism / Neutral |
| **Relevance** | **Bud Light** | 40 | **47.50%** | 12.50% | 40.00% | **-0.0915** | **0.3489** | 25.00% | 0.00% | 0.00% | 7.50% | 25.00% | 30.00% | Skepticism / Neutral |
| | | | | | | | | | | | | | | |
| **Unfiltered** | **Chick-fil-A** | 150 | 43.33% | 20.67% | 36.00% | -0.0083 | 0.2854 | 18.00% | 3.33% | 3.33% | 5.33% | 26.67% | 38.00% | Skepticism / Neutral |
| **Filtered** | **Chick-fil-A** | 78 | 46.15% | 23.08% | 30.77% | -0.0652 | 0.2823 | 20.51% | 2.56% | 5.13% | 2.56% | 24.36% | 39.74% | Skepticism / Neutral |
| **Relevance** | **Chick-fil-A** | 54 | **50.00%** | 16.67% | 33.33% | **-0.0706** | **0.2936** | 20.37% | **3.70%** | **7.41%** | 0.00% | 27.78% | 33.33% | Skepticism / Neutral |
| | | | | | | | | | | | | | | |
| **Unfiltered** | **Target** | 1,291 | 56.93% | 12.78% | 30.29% | -0.1972 | 0.3430 | 23.01% | 0.39% | 3.25% | 28.12% | 15.57% | 27.19% | Fear / Concern |
| **Filtered** | **Target** | 1,129 | 56.69% | 13.29% | 30.03% | -0.1996 | 0.3376 | 21.61% | 0.35% | 3.10% | 28.61% | 14.88% | 29.14% | Skepticism / Neutral |
| **Relevance** | **Target** | 685 | **59.71%** | 10.66% | 29.64% | **-0.2172** | **0.3549** | 20.73% | 0.44% | 4.82% | **34.60%** | 15.04% | 22.04% | **Fear / Concern** |

---

## 3. Análise Detalhada Por Marca

### A. Bud Light: Concentração da Polarização Ideológica
* **Variação da Amostra**: De $170$ comentários para $94$ (Filtrada) e $40$ (Relevância auditada).
* **Efeito da Filtragem**: Na base de relevância auditada, o indicador de **Hostilidade (OHI)** atinge o maior patamar (**0,3489** vs **0,2918** na não filtrada).
* **Interpretação**: A remoção de comentários genéricos ("eu nem bebo cerveja", "cerveja de milho") deixou sob holofote a verdadeira disputa ideológica entre os boicotadores conservadores e os defensores da marca / Dylan Mulvaney.

### B. Chick-fil-A: O Despertar da Decepção e Traição
* **Variação da Amostra**: De $150$ comentários para $78$ (Filtrada) e $54$ (Relevância auditada).
* **Efeito da Filtragem**: A taxa de comentários **Negativos** cresce de $43,33\%$ para **$50,00\%$**, enquanto **Decepção** atinge **$7,41\%$** e **Traição** chega a **$3,70\%$**.
* **Interpretação**: O ruído de conversas triviais sobre fast-food mascarava a gravidade da perda de capital de confiança junto à base conservadora tradicional quando a marca alterou suas diretrizes de doações de caridade.

### C. Target: Foco Crítico na Violência e Segurança dos Trabalhadores
* **Variação da Amostra**: De $1.291$ comentários para $1.129$ (Filtrada) e $685$ (Relevância auditada).
* **Efeito da Filtragem**: O **Medo / Preocupação com Segurança** cresce substancialmente de **$28,12\%$** para **$34,60\%$**, tornando-se a emoção amplamente dominante no corpus relevante.
* **Interpretação**: A base auditada de relevância filtra discussões gerais sobre compras na Target e isola os discursos de indignação com o recuo corporativo perante ameaças extremistas e segurança dos funcionários nas lojas.

---

## 4. Evolução dos Tópicos LDA e N-Grams

A filtragem também aprimorou a consistência léxica das modelagens de tópicos (LDA) e N-Grams:

* **Bud Light**:
  * *Não Filtrada*: `[beer, light, bud, just, fuck]`
  * *Relevância Auditada*: `[campaign, sales, formal, backs, products, bud]` (Foco direto no impacto comercial e recuo do marketing).
* **Chick-fil-A**:
  * *Não Filtrada*: `[food, better, lol, thing, Popeyes]`
  * *Relevância Auditada*: `[chickfila, worked, donating, groups, reason, left]` (Foco nas doações corporativas e posições políticas).
* **Target**:
  * *Não Filtrada*: `[target, pride, like, right, just]`
  * *Relevância Auditada*: `[win, target, terrorists, cave, threats, stand]` (Foco na discussão sobre ceder a ameaças e terrorismo doméstico).

---

## 5. Arquivos Gerados e Localização das Visualizações

### Planilhas Excel Atualizadas:
- **Comparação Geral**: [`output/master/NLP_Dataset_Comparison.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/NLP_Dataset_Comparison.xlsx)
- **Base Não Filtrada Atualizada**: [`output/master/Reddit_Master_NLP_Unfiltered.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/Reddit_Master_NLP_Unfiltered.xlsx)
- **Base Filtrada Atualizada**: [`output/master/Reddit_Master_NLP_Filtered.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/Reddit_Master_NLP_Filtered.xlsx)
- **Base de Relevância Atualizada**: [`output/master/Reddit_Master_NLP_Relevance.xlsx`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/master/Reddit_Master_NLP_Relevance.xlsx)

### Visualizações Gráficas:
- **Gráficos Comparativos**: [`output/plots_comparison/`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots_comparison)
  - `01_comment_counts_comparison.png` (Redução amostral por filtragem)
  - `02_negative_sentiment_shift.png` (Aumento da negatividade com a filtragem)
  - `03_hostility_index_comparison.png` (Evolução do Índice de Hostilidade OHI)
  - `04_focal_emotions_comparison.png` (Comparação das emoções de ultraje)
- **Gráficos por Base**:
  - Base Não Filtrada: [`output/plots_unfiltered/`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots_unfiltered)
  - Base Filtrada: [`output/plots_filtered/`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots_filtered)
  - Base de Relevância: [`output/plots_relevance/`](file:///Users/rtjaiany/Documents/01%20-%20In%20Progress/scrapping_reddit/output/plots_relevance)
