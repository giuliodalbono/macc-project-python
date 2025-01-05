from datetime import datetime

from sqlalchemy import ForeignKey

from db import db
from sqlalchemy.orm import Mapped, mapped_column


class Message(db.db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    translation: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column()
    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'), nullable=False)
    creation_time: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    last_update: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())

    def to_dict(self):
        return {"id": self.id, "message": self.message, "translation": self.translation, "city": self.city,
                "chat_id": self.chat_id, "creation_time": self.creation_time, "last_update": self.last_update}
