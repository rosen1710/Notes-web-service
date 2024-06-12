from sqlalchemy import Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class Note(Base):
    __tablename__ = "note"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    date_time: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.date_time = datetime.now()