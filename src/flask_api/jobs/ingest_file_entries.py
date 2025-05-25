import os
import json
from flask_api.app import db
from flask_api.models.file_entry import FileEntry

NEW_DATA_DIR = "/home/phuong/Desktop/thuc_tap/json_doc"  # thư mục mới chứa json

def ingest_new_file_entry_jsons():
    for filename in os.listdir(NEW_DATA_DIR):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(NEW_DATA_DIR, filename)

        # Kiểm tra nếu đã ingest file này
        if FileEntry.query.filter_by(name=filename).first():
            continue

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            entries = [
                FileEntry(
                    name=item.get("name"),
                    path=item.get("path"),
                    filetype=item.get("filetype"),
                    system_dir=item.get("system_dir"),
                )
                for item in data.get("files", [])
            ]

            db.session.bulk_save_objects(entries)
            db.session.commit()
            print(f"Đã ghi {len(entries)} dòng từ {filename} vào DB")
        except Exception as e:
            db.session.rollback()
            print(f"Lỗi khi xử lý {filename}: {e}")
