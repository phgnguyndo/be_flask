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
        if not filename.endswith(".json"):
            continue

        # Kiểm tra xem file đã được xử lý chưa dựa trên filename trong DB
        if News.query.filter_by(filename=filename).first():
            print(f"File {filename} đã được xử lý, bỏ qua.")
            continue

        filepath = os.path.join(NEWS_JSON_FOLDER, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    news = News(
                        title=item.get("title"),
                        content=item.get("content"),
                        group=item.get("group"),
                        timestamp=datetime.fromisoformat(item.get("timestamp").replace("Z", "+00:00")),
                        filename=filename
                    )
                    db.session.add(news)
                db.session.commit()
                print(f"Đã xử lý file {filename} thành công.")
        except Exception as e:
            db.session.rollback()
            print(f"Lỗi khi ingest file {filename}: {e}")