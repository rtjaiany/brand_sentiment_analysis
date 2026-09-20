# Reddit Comment Scraper for Brand Controversy Analysis

This project automates the extraction of all public comments from 28 specific Reddit posts across three major controversy cases:
1. **Chick-fil-A** (10 URLs)
2. **Bud Light** (5 URLs)
3. **Target** (13 URLs)

---

## Key Features & Safety Mechanisms

- **IP Protection & Rate Limiting**: Enforces randomized throttling delays (`3.0s - 5.0s`) between post navigations, preventing IP rate-limiting or network blocks from Reddit security filters.
- **Stealth Headless Browser**: Built with Playwright Chromium automation using realistic browser profiles and User-Agent rotation.
- **Deep Comment Tree Parsing**: Extracts nested `<shreddit-comment>` elements, author metadata, upvote scores, dates, times, parent IDs, and permalinks.
- **Multi-Level Excel Export**:
  - `output/individual/`: Contains `.xlsx` files for every single post.
  - `output/cases/`: Contains consolidated `.xlsx` files for each case (`ChickFilA_All_Comments.xlsx`, `BudLight_All_Comments.xlsx`, `Target_All_Comments.xlsx`).
  - `output/master/`: Contains `Reddit_Master_Scraped_Comments.xlsx` with dedicated sheets per case and a global `Summary` sheet.

---

## Dataset Schema

Each generated `.xlsx` spreadsheet includes the following columns:

| Column Header | Description |
| :--- | :--- |
| `Case` | Brand case category (`Chick-fil-A`, `Bud Light`, `Target`) |
| `Search Query` | Original search query corresponding to the post |
| `Subreddit` | Target subreddit name (e.g., `Conservative`, `lgbt`, `news`) |
| `Post Title` | Full title of the Reddit post |
| `Post ID` | Post ID string (e.g., `dyanoy`, `137lnig`) |
| `Post URL` | Full canonical link to the Reddit post |
| `Comment ID` | Unique Reddit comment ID (e.g., `t1_f80h8xy`) |
| `Parent ID` | Parent comment/post ID |
| `Comment Depth` | Indentation level (0 = top-level reply, 1+ = nested reply) |
| `User / Author` | Reddit author username |
| `Upvotes / Score` | Net upvote score |
| `Comment Text` | Complete comment body text |
| `Date (UTC)` | Date in `YYYY-MM-DD` format |
| `Time (UTC)` | Time in `HH:MM:SS` format |
| `Created UTC (Timestamp)` | Standard Unix epoch timestamp |
| `Is Edited` | `Yes` or `No` |
| `Permalink` | Direct link to the comment |

---

## Project Structure

```
scrapping_reddit/
├── reddit_scraper.py      # Main executable scraper script
├── scraper.log            # Execution log file
├── README.md              # Project documentation
└── output/
    ├── individual/        # 28 individual post Excel files
    ├── cases/             # 3 case summary Excel files
    └── master/            # Master Excel workbook with all data
```

---

## Running the Scraper

To run the script manually:

```bash
python3 reddit_scraper.py
```
