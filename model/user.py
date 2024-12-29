from app import db


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "username": self.username}
