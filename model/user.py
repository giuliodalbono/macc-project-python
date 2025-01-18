from datetime import datetime

from db import db
from sqlalchemy.orm import Mapped, mapped_column


class User(db.db.Model):
    uid: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    target_language: Mapped[str] = mapped_column(nullable=False)
    creation_time: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    last_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())

    def to_dict(self):
        return {"uid": self.uid, "email": self.email, "username": self.username, "target_language": self.target_language,
                "creation_time": self.creation_time, "last_update": self.last_update}
