"""
Reddit Comment Scraper for Brand Controversies (Chick-fil-A, Bud Light, Target)

Features:
- Stealth Playwright headless browser automation with anti-blocking safeguards
- Rate limiting with randomized delays (3.0s - 5.0s) to avoid IP blocks
- Network idle hydration & selector waiting for full comment loading
- Parses deep nested comments, score, author, timestamps, permalinks, and bodies
- Exports results to structured Excel (.xlsx) files:
  1. Individual files per post URL (`output/individual/`)
  2. Consolidated files per case (`output/cases/`)
  3. Master Excel workbook (`output/master/Reddit_Master_Scraped_Comments.xlsx`)
"""

import os
import re
import time
import random
import logging
import asyncio
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# -----------------------------------------------------------------------------
# TARGET POST CATALOG (28 URLs categorized by Case and Search Query)
# -----------------------------------------------------------------------------
TARGET_POSTS = [
    # -------------------------------------------------------------------------
    # CASE: Chick-fil-A (10 URLs)
    # -------------------------------------------------------------------------
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "stopped donating" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/Conservative/comments/dyanoy/chickfila_will_stop_donating_to_salvation_army/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "stopped donating" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/Christianity/comments/dym4u5/chick_fil_a_to_stop_donations_to_antilgbqt/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "stopped donating" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/atheism/comments/emujvu/chick_fil_a_stopped_donations_to_fellowship_of/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "stopped donating" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/TraditionalCatholics/comments/dyi17r/chickfila_will_stop_donating_money_to_charities/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "stopped donating" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/lgbt/comments/e1sfse/since_chick_fila_stopped_donating_to_salvation/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "stopped donating" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/TheRightBoycott/comments/dya3jt/rip_chickfila/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "ended donations" AND FCA',
        "url": "https://www.reddit.com/r/ChickFilAWorkers/comments/dy6h71/chickfila_is_ending_donations_to_antilgbtq_groups/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "ended donations" AND FCA',
        "url": "https://www.reddit.com/r/LGBTnews/comments/dy6kgt/chickfila_is_ending_donations_criticized_by_lgbtq/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "ended donations" AND FCA',
        "url": "https://www.reddit.com/r/atlanticdiscussions/comments/dykc28/chikfila_will_no_longer_donate_to_antilgbt_causes/"
    },
    {
        "case": "Chick-fil-A",
        "query": '"Chick-fil-A" AND "dropped support" AND "Salvation Army"',
        "url": "https://www.reddit.com/r/Reformed/comments/dy9bx6/chickfila_drops_support_for_fca_and_salvation_army/"
    },

    # -------------------------------------------------------------------------
    # CASE: Bud Light (5 URLs)
    # -------------------------------------------------------------------------
    {
        "case": "Bud Light",
        "query": '"Bud Light" + distancing',
        "url": "https://www.reddit.com/r/Conservative/comments/137lnig/ceo_distances_anheuserbusch_from_bud_light_dylan/"
    },
    {
        "case": "Bud Light",
        "query": '"Bud Light" + "stay in our lane"',
        "url": "https://www.reddit.com/r/transgender/comments/1cmz9gs/cowardly_bud_light_to_stay_in_our_lane_after/"
    },
    {
        "case": "Bud Light",
        "query": '"Anheuser-Busch" AND statement AND Mulvaney',
        "url": "https://www.reddit.com/r/trump/comments/12mpanj/anheuserbusch_puts_out_a_new_statement_on_dylan/"
    },
    {
        "case": "Bud Light",
        "query": '"Bud Light" due diligence',
        "url": "https://www.reddit.com/r/wallstreetbets/comments/15forkm/bud_due_dilligence/"
    },
    {
        "case": "Bud Light",
        "query": '"Bud Light" AND abandoned AND Mulvaney',
        "url": "https://www.reddit.com/r/Conservative/comments/13aoa1y/bud_lights_dylan_mulvaney_controversy_deepens/"
    },

    # -------------------------------------------------------------------------
    # CASE: Target (13 URLs)
    # -------------------------------------------------------------------------
    {
        "case": "Target",
        "query": '"Target" AND "Pride collection" AND removed',
        "url": "https://www.reddit.com/r/lgbt/comments/13qvbna/response_from_the_artist_abprallen_regarding_his/"
    },
    {
        "case": "Target",
        "query": '"Target" AND "Pride collection" AND removed',
        "url": "https://www.reddit.com/r/hudsonvalley/comments/13wrfw2/kingston_companys_products_removed_from_target/"
    },
    {
        "case": "Target",
        "query": '"Target" AND "Pride collection" AND removed',
        "url": "https://www.reddit.com/r/Target/comments/13qqxs0/target_caving_to_bigots/"
    },
    {
        "case": "Target",
        "query": '"Target" AND "Pride collection" AND removed',
        "url": "https://www.reddit.com/r/Conservative/comments/13rw5iq/exclusive_target_warns_of_extremists_violence_in/"
    },
    {
        "case": "Target",
        "query": '"Target" AND "Pride collection" AND removed',
        "url": "https://www.reddit.com/r/Target/comments/13qaael/sad_this_is_the_world_we_live_in/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/lgbt/comments/13qq2c5/target_is_removing_pride_products_because_the/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/democrats/comments/13vigj7/target_has_removed_pride_apparel_that_the_cpac/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/news/comments/13q6rg9/target_removes_some_lgbtq_merchandise_from_stores/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/FreeSpeech/comments/13sy8xa/cancel_culture_target_removes_pride_merch_after/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/WhitePeopleTwitter/comments/13qjxu4/threats_to_target_workers_forced_target_to_remove/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/askgaybros/comments/13q9ddh/target_caves_in_to_right_wing_pressure_and_is/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/lgbt/comments/13qbl03/target_removes_some_lgbtq_merchandise_from_stores/"
    },
    {
        "case": "Target",
        "query": '"Target" AND Pride AND remove',
        "url": "https://www.reddit.com/r/LGBTnews/comments/13soa3m/the_mistake_target_made_by_removing_pride_items/"
    }
]

# User Agent Rotation Pool
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
]

def parse_url_details(url: str):
    """Extracts subreddit and post_id from Reddit URL."""
    match = re.search(r'reddit\.com/r/([^/]+)/comments/([^/]+)', url)
    if match:
        return match.group(1), match.group(2)
    return "unknown", "unknown"

def format_timestamp(ts_str):
    """Converts ISO timestamp string to Date (UTC), Time (UTC), and unix timestamp."""
    if not ts_str:
        return "", "", ""
    try:
        dt = datetime.fromisoformat(ts_str.replace('+0000', '+00:00'))
        date_utc = dt.strftime('%Y-%m-%d')
        time_utc = dt.strftime('%H:%M:%S')
        unix_ts = int(dt.timestamp())
        return date_utc, time_utc, unix_ts
    except Exception:
        return ts_str, "", ""

async def scrape_single_post(page, target: dict) -> tuple[str, list[dict]]:
    """
    Scrapes a single post page using Playwright.
    Includes network idle waiting, comment expansion, rate-limiting delays, and shreddit-comment extraction.
    """
    url = target['url']
    case = target['case']
    query = target['query']
    subreddit, post_id = parse_url_details(url)

    logging.info(f"Navigating to [{case}] {url}...")

    # Throttling delay between post visits to protect IP
    delay = random.uniform(3.0, 5.0)
    await asyncio.sleep(delay)

    try:
        # Load page until network is idle so web components hydrate
        response = await page.goto(url, wait_until='networkidle', timeout=45000)
        if response and response.status != 200:
            logging.warning(f"HTTP Status {response.status} for {url}")
        
        # Wait specifically for shreddit-comment element
        try:
            await page.wait_for_selector('shreddit-comment', timeout=15000)
        except Exception:
            logging.debug("shreddit-comment selector wait timed out, continuing...")

    except Exception as e:
        logging.error(f"Failed to navigate to {url}: {e}")
        return "Unknown Title", []

    # Get Post Title
    try:
        title = await page.title()
        title = re.sub(r'\s*:\s*r/[A-Za-z0-9_]+\s*$', '', title).strip()
    except Exception:
        title = "Unknown Title"

    # Scroll to load comments dynamically
    logging.info(f"Loading comments for post: {title[:60]}...")
    previous_count = 0
    for i in range(12):
        await page.evaluate('window.scrollBy(0, 2000)')
        await page.wait_for_timeout(1000)

        # Expand hidden comment threads if present
        more_btns = await page.query_selector_all(
            'button:has-text("more comment"), button:has-text("View more comments"), faceplate-tracker[label="more_comments"]'
        )
        for btn in more_btns[:3]:
            try:
                if await btn.is_visible():
                    await btn.click()
                    await page.wait_for_timeout(600)
            except Exception:
                pass

        current_count = len(await page.query_selector_all('shreddit-comment'))
        if current_count == previous_count and i > 4:
            break
        previous_count = current_count

    comments_nodes = await page.query_selector_all('shreddit-comment')
    logging.info(f"Extracted {len(comments_nodes)} comments from {subreddit}/{post_id}")

    extracted_records = []
    for node in comments_nodes:
        try:
            attrs = await node.evaluate('el => { const res = {}; for (let a of el.attributes) res[a.name] = a.value; return res; }')
            
            author = attrs.get('author', '[unknown]')
            score = attrs.get('score', '0')
            thing_id = attrs.get('thingid', '')
            depth = attrs.get('depth', '0')
            created_raw = attrs.get('created', '')
            permalink = attrs.get('permalink', '')
            if permalink and not permalink.startswith('http'):
                permalink = f"https://www.reddit.com{permalink}"

            # Extract body text paragraphs
            paragraphs = await node.query_selector_all('p')
            if paragraphs:
                p_texts = [await p.inner_text() for p in paragraphs]
                comment_text = "\n\n".join([p.strip() for p in p_texts if p.strip()])
            else:
                raw_text = await node.inner_text()
                comment_text = raw_text.strip()

            date_utc, time_utc, timestamp_utc = format_timestamp(created_raw)

            record = {
                "Case": case,
                "Search Query": query,
                "Subreddit": subreddit,
                "Post Title": title,
                "Post ID": post_id,
                "Post URL": url,
                "Comment ID": thing_id,
                "Parent ID": attrs.get('parent-id', ''),
                "Comment Depth": int(depth) if str(depth).isdigit() else depth,
                "User / Author": author,
                "Upvotes / Score": int(score) if str(score).lstrip('-').isdigit() else score,
                "Comment Text": comment_text,
                "Date (UTC)": date_utc,
                "Time (UTC)": time_utc,
                "Created UTC (Timestamp)": timestamp_utc,
                "Is Edited": "Yes" if attrs.get('edited') else "No",
                "Permalink": permalink
            }
            extracted_records.append(record)

        except Exception as err:
            logging.debug(f"Error parsing single comment node: {err}")
            continue

    return title, extracted_records


async def main():
    logging.info("Starting Reddit Comment Scraper (Stealth Playwright Mode)...")

    # Ensure output directories exist
    os.makedirs("output/individual", exist_ok=True)
    os.makedirs("output/cases", exist_ok=True)
    os.makedirs("output/master", exist_ok=True)

    all_scraped_records = []

    async with async_playwright() as p:
        user_agent = random.choice(USER_AGENTS)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1280, 'height': 900},
            locale='en-US'
        )
        page = await context.new_page()

        for idx, target in enumerate(TARGET_POSTS, start=1):
            logging.info(f"--- Processing [{idx}/{len(TARGET_POSTS)}] ---")
            title, records = await scrape_single_post(page, target)
            
            subreddit, post_id = parse_url_details(target['url'])
            case_slug = target['case'].replace(" ", "_")

            if records:
                all_scraped_records.extend(records)
                df_post = pd.DataFrame(records)

                # Export individual post Excel file
                filename_ind = f"output/individual/{case_slug}_{subreddit}_{post_id}.xlsx"
                with pd.ExcelWriter(filename_ind, engine='openpyxl') as writer:
                    df_post.to_excel(writer, index=False, sheet_name="Comments")
                logging.info(f"Saved {len(records)} comments to {filename_ind}")

            else:
                logging.warning(f"No comments extracted for {target['url']}")

        await browser.close()

    if not all_scraped_records:
        logging.error("No records collected across all target posts.")
        return

    df_all = pd.DataFrame(all_scraped_records)

    # Export Case Consolidated Excel Files
    for case_name, df_case in df_all.groupby("Case"):
        case_slug = str(case_name).replace(" ", "_")
        filename_case = f"output/cases/{case_slug}_All_Comments.xlsx"
        with pd.ExcelWriter(filename_case, engine='openpyxl') as writer:
            df_case.to_excel(writer, index=False, sheet_name=str(case_name))
        logging.info(f"Saved {len(df_case)} total comments for case [{case_name}] to {filename_case}")

    # Export Master Consolidated Excel File (Multiple Worksheets per Case)
    master_path = "output/master/Reddit_Master_Scraped_Comments.xlsx"
    with pd.ExcelWriter(master_path, engine='openpyxl') as writer:
        for case_name, df_case in df_all.groupby("Case"):
            sheet_title = str(case_name)[:31]
            df_case.to_excel(writer, index=False, sheet_name=sheet_title)
        
        # Summary tab
        summary_data = []
        for case_name, df_case in df_all.groupby("Case"):
            summary_data.append({
                "Case": case_name,
                "Total Posts": df_case['Post ID'].nunique(),
                "Total Comments": len(df_case),
                "Unique Authors": df_case['User / Author'].nunique()
            })
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, index=False, sheet_name="Summary")

    logging.info(f"SUCCESS: Master workbook created at {master_path}")
    print("\n========================================================")
    print(f"SCRAPING COMPLETE! Total comments extracted: {len(df_all)}")
    print(f"Master Excel file: {master_path}")
    print("========================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
