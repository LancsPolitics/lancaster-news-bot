name: Lancaster Wyre News Bot

on:
  schedule:
    - cron: '0 8,12,16,20 * * *'
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Show me what files exist
        run: |
          echo "Current folder contents:"
          ls -la
          echo ""
          echo "Looking for bot.py..."
          ls -la bot.py || echo "bot.py is MISSING"

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install packages
        run: pip install feedparser google-generativeai

      - name: Run the bot
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python bot.py
