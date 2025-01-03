from sqlalchemy import ForeignKey

from db import db
from sqlalchemy.orm import Mapped, mapped_column


class Chat(db.db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    is_public: Mapped[bool] = mapped_column(nullable=False, default=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('user.uid'), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "is_public": self.is_public, "user_id": self.user_id}
