import feedparser
import google.generativeai as genai
import os
from datetime import datetime

# Free Gemini AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Local news search
rss_url = "https://news.google.com/rss/search?q=%22Lancaster%22+OR+Wyre+OR+Morecambe+OR+Fleetwood+OR+%22Poulton-le-Fylde%22+Lancashire&hl=en-GB&gl=GB&ceid=GB:en"

feed = feedparser.parse(rss_url)

tweets = []
for entry in feed.entries[:6]:  # take the 6 newest stories
    title = entry.title
    link = entry.link

    prompt = f"""
    Write a short, natural, friendly tweet about this local news story from Lancaster or Wyre.
    Keep it under 260 characters.
    Include the link at the end.
    Do not use hashtags unless they feel natural.
    Story title: {title}
    Link: {link}
    """

    response = model.generate_content(prompt)
    tweet = response.text.strip()
    tweets.append(tweet)

# Save the tweets to a file
with open("todays_tweets.txt", "w") as f:
    f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    for i, t in enumerate(tweets, 1):
        f.write(f"Tweet {i}:\n{t}\n\n-------------------\n\n")

print("Done! Tweets saved to todays_tweets.txt")
