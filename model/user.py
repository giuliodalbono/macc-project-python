from db import db
from sqlalchemy.orm import Mapped, mapped_column


class User(db.db.Model):
    uid: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)

    def to_dict(self):
        return {"uid": self.uid, "email": self.email, "username": self.username}
