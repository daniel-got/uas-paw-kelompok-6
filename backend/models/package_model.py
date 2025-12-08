import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from .base import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    destination_id = Column(
        UUID(as_uuid=True), ForeignKey("destinations.id"), nullable=False, index=True
    )
    name = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)  # in days
    price = Column(Numeric(10, 2), nullable=False)  # decimal for currency
    itinerary = Column(Text, nullable=False)
    max_travelers = Column(Integer, nullable=False)
    contact_phone = Column(String(20), nullable=False)
    images = Column(ARRAY(String), nullable=False)  # PostgreSQL array of image URLs

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    agent = relationship("User", back_populates="packages")
    destination = relationship("Destination", back_populates="packages")
    bookings = relationship("Booking", back_populates="package")
    reviews = relationship("Review", back_populates="package")
