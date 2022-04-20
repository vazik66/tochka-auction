from app.db.base_class import Base

from sqlalchemy import Column, Boolean, String, ForeignKey, Integer, DateTime, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class Item(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    is_archived = Column(Boolean(), nullable=False, server_default="false")
    is_moderating = Column(Boolean(), nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    images = Column(ARRAY(String), server_default="{}")
