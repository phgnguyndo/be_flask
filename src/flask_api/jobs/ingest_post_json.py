import os
import json
from datetime import datetime
from flask import jsonify
from flask_api.models.post_entry import PostEntry
from flask_api.app import db
from config.settings import Config

def parse_datetime(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

def ingest_post_json_files():
    upload_dir = Config.UPLOAD_JSON
    ingested_count = 0
    skipped_files = []

    for filename in os.listdir(upload_dir):
        if not filename.endswith('.json'):
            continue

        # Đã ingest rồi thì bỏ qua
        if PostEntry.query.filter_by(filename=filename).first():
            skipped_files.append(filename)
            continue

        filepath = os.path.join(upload_dir, filename)
        try:
            with open(filepath, 'r') as f:
                records = json.load(f)

            for rec in records:
                entry = PostEntry(
                    post_title=rec.get("post_title"),
                    group_name=rec.get("group_name"),
                    discovered=parse_datetime(rec.get("discovered")),
                    description=rec.get("description"),
                    published=parse_datetime(rec.get("published")),
                    post_url=rec.get("post_url"),
                    country=rec.get("country"),
                    activity=rec.get("activity"),
                    website=rec.get("website"),
                    filename=filename
                )

                db.session.add(entry)

            db.session.commit()
            ingested_count += 1
        except Exception as e:
            db.session.rollback()
            print(f"Error ingest file {filename}: {e}")
            continue

    return jsonify({
        'success': True,
        'ingested_files': ingested_count,
        'skipped_files': skipped_files
    })
