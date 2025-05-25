import sys
import os

# Thêm đường dẫn src/ vào sys.path để Python biết tìm module ở đó
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask_api import create_app
from flask_api.app import db
from flask_api.models.credential import Credential
from flask_api.jobs.ingest_json import ingest_new_json_files

from flask_apscheduler import APScheduler

app = create_app()

with app.app_context():
    db.create_all()

     # Thiết lập APScheduler
    scheduler = APScheduler()
    scheduler.init_app(app)

    # Lập lịch ingest lúc 19h hàng ngày
    @scheduler.task("cron", id="daily_ingest", hour=19, minute=0)
    def scheduled_ingest():
        print("[Scheduler] Bắt đầu ingest file JSON lúc 19h...")
        ingest_new_json_files()

    scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
