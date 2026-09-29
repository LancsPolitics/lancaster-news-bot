import os
from datetime import datetime

import feedparser
from google import genai
from google.genai import types

api_key = os.environ["GEMINI_API_KEY"].strip()
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is empty")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=60_000,  # 60 seconds, rather than allowing a 10-minute retry
    ),
)

model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

rss_url = (
    "https://news.google.com/rss/search?"
    "q=%22Lancaster%22+OR+Wyre+OR+Morecambe+OR+Fleetwood+OR+"
    "%22Poulton-le-Fylde%22+Lancashire&hl=en-GB&gl=GB&ceid=GB:en"
)

feed = feedparser.parse(rss_url)
tweets = []

for entry in feed.entries[:6]:
    prompt = f"""
Write a short, natural, friendly tweet about this local news story from
Lancaster or Wyre. Keep it under 260 characters. Include the link at the end.
Do not use hashtags unless they feel natural.

Story title: {entry.title}
Link: {entry.link}
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        tweet = (response.text or "").strip()

        if tweet:
            tweets.append(tweet)
    except Exception as exc:
        # Do not abort the whole scheduled job because one request failed.
        print(f"Could not generate tweet for {entry.title!r}: {exc}")

with open("todays_tweets.txt", "w", encoding="utf-8") as output:
    output.write(
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    )
    for i, tweet in enumerate(tweets, 1):
        output.write(
            f"Tweet {i}:\n{tweet}\n\n-------------------\n\n"
        )

print(f"Done! Generated {len(tweets)} tweets.")
