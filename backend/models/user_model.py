import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # bcrypt hashed
    role = Column(Enum("tourist", "agent", "guide", name="user_role"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    bookings = relationship(
        "Booking", back_populates="tourist", foreign_keys="Booking.tourist_id"
    )
    packages = relationship("Package", back_populates="agent")
    reviews = relationship("Review", back_populates="tourist")
    guide_tasks = relationship("TourGuideAssignment", back_populates="guide")
