from flask_api.app import db

class PostEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.Text)
    group_name = db.Column(db.String(255))
    discovered = db.Column(db.DateTime)
    description = db.Column(db.Text)
    published = db.Column(db.DateTime)
    post_url = db.Column(db.String(512))
    country = db.Column(db.String(10))
    activity = db.Column(db.String(255))
    website = db.Column(db.String(512))
    filename = db.Column(db.String(255))

    def to_dict(self):
        return {
            "post_title": self.post_title,
            "group_name": self.group_name,
            "discovered": self.discovered.isoformat() if self.discovered else None,
            "description": self.description,
            "published": self.published.isoformat() if self.published else None,
            "post_url": self.post_url,
            "country": self.country,
            "activity": self.activity,
            "website": self.website,
            "filename": self.filename
        }
