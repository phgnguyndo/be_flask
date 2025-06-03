import os
import json
from datetime import datetime
from flask_api.app import db
from flask_api.models.news import News
from dotenv import load_dotenv

load_dotenv()
NEWS_JSON_FOLDER = os.getenv("NEWS_JSON_FOLDER")

def ingest_news_json():
    for filename in os.listdir(NEWS_JSON_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(NEWS_JSON_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    items = json.load(f)
                    for item in items:
                        news = News(
                            title=item.get("title"),
                            content=item.get("content"),
                            group=item.get("group"),
                            timestamp=datetime.fromisoformat(item.get("timestamp").replace("Z", "+00:00"))
                        )
                        db.session.add(news)
                    db.session.commit()
                except Exception as e:
                    print(f"Lỗi khi ingest file {filename}: {e}")
