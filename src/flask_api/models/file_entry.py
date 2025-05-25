from flask_api.app import db

class FileEntry(db.Model):
    __tablename__ = "file_entries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.Text, nullable=False)
    filetype = db.Column(db.String(50), nullable=True)
    system_dir = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<FileEntry {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "filetype": self.filetype,
            "system_dir": self.system_dir
        }
