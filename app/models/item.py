from app.db.base_class import Base

from sqlalchemy import Column, Boolean, String, ForeignKey, Integer, DateTime, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Item(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    min_bid = Column(Integer, nullable=False)
    min_bid_step = Column(Integer, server_default="1")
    is_archived = Column(Boolean(), nullable=False, server_default="false")
    is_ended = Column(Boolean(), nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=False)
    images = Column(ARRAY(String), server_default="{}")
    bids = relationship("Bid", backref="item", lazy="select")
    winner = Column(UUID(as_uuid=True), ForeignKey("user.id"))
