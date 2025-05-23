from flask_api.app import db

class Credential(db.Model):
    __tablename__ = "credentials"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=True)
    system = db.Column(db.String(255), nullable=True)

    software = db.Column(db.String(255), nullable=True)
    host = db.Column(db.String(512), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    domain = db.Column(db.String(255), nullable=True)
    local_part = db.Column(db.String(255), nullable=True)
    email_domain = db.Column(db.String(255), nullable=True)
    filepath = db.Column(db.Text, nullable=True)
    stealer_name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Credential {self.username}@{self.domain}>"
