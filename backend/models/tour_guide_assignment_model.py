import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class TourGuideAssignment(Base):
    __tablename__ = "tour_guide_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("bookings.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    guide_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False, 
        index=True
    )
    status = Column(
        Enum("assigned", "on_duty", "completed", "cancelled", name="assignment_status"),
        nullable=False,
        default="assigned"
    )
    assigned_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    booking = relationship("Booking", back_populates="guide_assignments")
    guide = relationship("User", back_populates="guide_tasks")
