import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Text, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id = Column(
        UUID(as_uuid=True), ForeignKey("packages.id"), nullable=False, index=True
    )
    tourist_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    booking_id = Column(
        UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=True, index=True
    )
    rating = Column(Integer, nullable=False)  # 1–5
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

    # Relationships
    package = relationship("Package", back_populates="reviews")
    tourist = relationship("User", back_populates="reviews")
    booking = relationship("Booking", back_populates="review")

    # Constraints
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )
