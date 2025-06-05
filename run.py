import sys
import os

# Thêm đường dẫn src/ vào sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask_api import create_app
from flask_api.app import db
from flask_api.models.credential import Credential
from flask_api.models.file_entry import FileEntry
from flask_api.jobs.ingest_json import ingest_new_json_files
from flask_api.jobs.ingest_file_entries import ingest_new_file_entry_jsons
from flask_api.jobs.ingest_news import ingest_news_json
from flask_api.jobs.ingest_post_json import ingest_post_json_files
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

with app.app_context():
    db.create_all()

# Thiết lập APScheduler với múi giờ cụ thể
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Ho_Chi_Minh"))
scheduler.init_app(app)

# Lập lịch ingest lúc 19h hàng ngày
@scheduler.task("cron", id="daily_ingest", hour=19, minute=0)
def scheduled_ingest():
    with app.app_context():  # Thêm app.app_context()
        try:
            print("[Scheduler] ingest file JSON 19h...")
            ingest_new_json_files()
        except Exception as e:
            print(f"[Scheduler] Error ingest JSON: {e}")

@scheduler.task("cron", id="daily_ingest_file_entry", hour=19, minute=0)
def scheduled_ingest_file_entry():
    with app.app_context():  # Thêm app.app_context()
        try:
            print("[Scheduler] ingest FileEntry JSON 19h...")
            ingest_new_file_entry_jsons()
        except Exception as e:
            print(f"[Scheduler] Error ingest FileEntry JSON: {e}")

@scheduler.task("interval", id="daily_ingest_news", hours=2, minutes=30)
def scheduled_ingest_news():
    with app.app_context():
        try:
            print("[Scheduler] ingest News JSON every 2h30m...")
            ingest_news_json()
        except Exception as e:
            print(f"[Scheduler] Error ingest News JSON: {e}")

@scheduler.task("cron", id="daily_ingest_json_upload", hour=19, minute=0)
def scheduled_ingest_json_upload():
    with app.app_context():
        try:
            print("[Scheduler] ingest JSON upload 19h...")
            ingest_post_json_files()
        except Exception as e:
            print(f"[Scheduler] Error ingest JSON upload: {e}")

scheduler.start()

if __name__ == "__main__":
    print("[Scheduler] APScheduler đã được khởi động!")
    app.run(debug=True, use_reloader=False)  # Tắt reloader