import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Numeric,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Qris(Base):
    __tablename__ = "qris"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foto QR code file path (disimpan di storage/qris/)
    foto_qr_path = Column(String(500), nullable=False)
    
    # Static QRIS string (dari upload/scan gambar)
    static_qris_string = Column(String(500), nullable=False, unique=True)
    
    # Dynamic QRIS string (generated dengan fee)
    dynamic_qris_string = Column(String(500), nullable=False)
    
    # Fee configuration (optional)
    fee_type = Column(
        Enum("persentase", "rupiah", name="fee_type"),
        nullable=True,
    )
    fee_value = Column(Numeric(10, 2), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)
