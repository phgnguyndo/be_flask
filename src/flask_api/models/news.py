from flask_api.app import db
from datetime import datetime

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)  # dùng Text để không giới hạn độ dài
    group = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(255), index=True)  # Thêm trường filename với index

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "group": self.group,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "filename": self.filename
        }