from datetime import datetime, timezone
import uuid6
from sqlalchemy import Column, String, Float, Integer, DateTime

from app.database import Base


class PersonProfile(Base):
    __tablename__ = 'person_profile'

    id = Column(String, primary_key=True, default=lambda: str(uuid6.uuid7()), nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    gender_probability = Column(Float, nullable=False)
    sample_size = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    age_group = Column(String, nullable=False)
    country_id = Column(String, nullable=False)
    country_probability = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)