from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    created_dt = Column(DateTime, default=datetime.now(tz=timezone.utc))