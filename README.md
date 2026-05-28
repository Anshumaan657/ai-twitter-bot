**Here's the rewritten README.md with all hype removed:**

---

# AI Twitter/X Automation Bot

A Python-based system that fetches AI/ML articles from RSS feeds, generates tweets using Google Gemini, applies quality filtering and semantic deduplication, and supports Telegram-based approval workflows.

## Features

### News Aggregation
- RSS feed ingestion from multiple sources
- Basic article filtering and duplicate removal
- Simple ranking based on relevance signals

**Sources**
- TechCrunch AI
- OpenAI News
- Hugging Face Blog
- Google AI Blog
- BAIR Blog
- DeepMind Blog
- arXiv AI
- arXiv ML

### Tweet Generation
- Uses Google Gemini to generate tweet text
- Produces multiple variations per article
- Enforces character limits and basic formatting

### Semantic Memory System
- Uses sentence-transformers (`all-MiniLM-L6-v2`) to generate embeddings
- Applies cosine similarity to detect and reject repetitive or similar content

### Quality Validation
- Rejects tweets that are too long, repetitive, or low quality
- Basic scoring on originality, clarity, and relevance

### Storage
- SQLite database for articles, generated tweets, quality scores, and history

### Telegram Integration
- Sends generated tweets for review
- Supports approval/rejection via inline buttons

## System Architecture

```
RSS Feeds
   ↓
Article Parsing & Filtering
   ↓
Article Ranking
   ↓
Tweet Generation (Gemini)
   ↓
Quality Validation
   ↓
Semantic Similarity Check
   ↓
Database Storage
   ↓
Telegram Notification
```

## Project Structure

```
ai-twitter-bot/
├── main.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
├── services/
│   ├── gemini_service.py
│   ├── logger.py
│   ├── news_fetcher.py
│   ├── tweet_generator.py
│   ├── tweet_validator.py
│   ├── telegram_bot.py
│   ├── telegram_listener.py
│   ├── posting_engine.py
│   ├── posting_worker.py
│   ├── x_client.py
│   ├── database.py
│   └── memory_filter.py
│
├── data/
│   └── tweets.db
│
└── logs/
    └── bot.log
```

## Tech Stack

- **Language**: Python 3.12+
- **AI Model**: Google Gemini API
- **Libraries**:
  - `google-generativeai`
  - `requests`, `feedparser`
  - `sqlite3`
  - `sentence-transformers`
  - `scikit-learn`
  - `tweepy`
  - `python-telegram-bot`
  - `python-dotenv`

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
```

## Installation

git clone https://github.com/Anshumaan657/ai-twitter-bot.git
cd ai-twitter-bot


**Virtual Environment**


# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate


pip install -r requirements.txt

Run:
python main.py


## Logging

Logs are written to `logs/bot.log`.

## Current Status

**Completed**
- RSS news ingestion
- Article filtering and ranking
- Gemini-based tweet generation
- Quality validation pipeline
- Semantic deduplication
- SQLite persistence
- Telegram notification system

**In Progress**
- Approval workflow improvements
- Automated posting
- Scheduler implementation

## License

MIT License

## Author

Anshumaan Sharma
