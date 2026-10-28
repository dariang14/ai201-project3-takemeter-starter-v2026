"""
Collect raw candidate posts/comments from r/nba using Reddit's own read-only
API (via PRAW) — not scraping, not bot-detection circumvention.

Setup (one time, ~5 minutes):
  1. Go to https://www.reddit.com/prefs/apps, click "create app" / "create
     another app" at the bottom.
  2. Pick type "script". Name and description can be anything
     (e.g. "takemeter-collector"). For "redirect uri" put
     http://localhost:8080 — it's required but unused for this flow.
  3. After creating it, copy the client ID (the string under the app name,
     NOT labelled) and the "secret" field.
  4. Create a file named `.env` in this repo's root (it's already
     gitignored) with:

       REDDIT_CLIENT_ID=your_client_id_here
       REDDIT_CLIENT_SECRET=your_secret_here
       REDDIT_USER_AGENT=takemeter-collector by u/your_reddit_username

  5. pip install praw python-dotenv
  6. python collect_posts.py

Output: data/raw_collected.csv with columns id, source, text, permalink.
This is RAW, unlabelled, and will have duplicates/junk in it — it's meant to
be over-collected so you can filter down to your best ~200 while labelling.
You still read and label every row yourself (or review AI pre-labels and
correct them) — this script only replaces the copy-pasting, not the judgment.
"""

import os
import re
import csv
import sys

try:
    import praw
except ImportError:
    sys.exit("Missing dependency. Run: pip install praw python-dotenv")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # fine if the env vars are set another way

CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "takemeter-collector")

if not CLIENT_ID or not CLIENT_SECRET:
    sys.exit(
        "Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET.\n"
        "Create a .env file in this repo's root — see the instructions at "
        "the top of this file."
    )

SUBREDDIT = "nba"
OUT_PATH = os.path.join("data", "raw_collected.csv")

MIN_LEN = 15
MAX_LEN = 2000
SKIP_BODIES = {"[deleted]", "[removed]", ""}


def clean(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_usable(text):
    if text is None:
        return False
    t = clean(text)
    if t in SKIP_BODIES:
        return False
    if len(t) < MIN_LEN or len(t) > MAX_LEN:
        return False
    return True


def main():
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )
    reddit.read_only = True

    sub = reddit.subreddit(SUBREDDIT)
    rows = []
    seen = set()

    def add(id_, source, text, permalink):
        text = clean(text)
        if not is_usable(text) or text in seen:
            return
        seen.add(text)
        rows.append({"id": id_, "source": source, "text": text, "permalink": permalink})

    print("Pulling hot posts...")
    for post in sub.hot(limit=100):
        if post.stickied:
            continue
        title_and_body = post.title if not post.selftext else f"{post.title} — {post.selftext}"
        add(post.id, "hot_post", title_and_body, post.permalink)

    print("Pulling top posts (past month)...")
    for post in sub.top(time_filter="month", limit=100):
        if post.stickied:
            continue
        title_and_body = post.title if not post.selftext else f"{post.title} — {post.selftext}"
        add(post.id, "top_post_month", title_and_body, post.permalink)

    print("Pulling comments from the biggest recent threads (reactions/hot takes live here)...")
    thread_count = 0
    for post in sub.top(time_filter="week", limit=15):
        thread_count += 1
        post.comments.replace_more(limit=0)
        for comment in post.comments[:40]:
            add(comment.id, "comment", comment.body, comment.permalink)
        print(f"  thread {thread_count}: {len(rows)} usable rows so far")

    os.makedirs("data", exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "source", "text", "permalink"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} raw candidate rows to {OUT_PATH}")
    print("Next: label these (or have them pre-labelled) into labels.csv — "
          "see labels_template.csv for the shape.")


if __name__ == "__main__":
    main()
