import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Date,
    Text,
    Integer,
    Numeric,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id = Column(
        UUID(as_uuid=True), ForeignKey("packages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tourist_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    travel_date = Column(Date, nullable=False, index=True)
    travelers_count = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(
        Enum("pending", "confirmed", "cancelled", "completed", name="booking_status"),
        nullable=False,
        default="pending",
        index=True,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    completed_at = Column(DateTime, nullable=True)
    has_reviewed = Column(Boolean, default=False)

    # Payment fields
    payment_status = Column(
        Enum(
            "unpaid",
            "pending_verification",
            "verified",
            "rejected",
            name="payment_status",
        ),
        nullable=False,
        default="unpaid",
        index=True,
    )

    payment_proof_url = Column(String(500), nullable=True)
    payment_proof_uploaded_at = Column(DateTime, nullable=True)
    payment_verified_at = Column(DateTime, nullable=True)
    payment_rejection_reason = Column(Text, nullable=True)

    # Relationships
    package = relationship("Package", back_populates="bookings")
    tourist = relationship("User", back_populates="bookings", foreign_keys=[tourist_id])
    review = relationship("Review", back_populates="booking", uselist=False)
    guide_assignments = relationship("TourGuideAssignment", back_populates="booking")
