import sys
import os

# Thêm đường dẫn src/ vào sys.path để Python biết tìm module ở đó
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask_api import create_app
from flask_api.app import db
from flask_api.models.credential import Credential
from flask_api.jobs.ingest_json import ingest_new_json_files

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
