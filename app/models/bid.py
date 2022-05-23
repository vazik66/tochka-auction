from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Bid(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    item_id = Column(UUID(as_uuid=True), ForeignKey("item.id"))
    amount = Column(
        Integer,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", backref="bid", lazy="select")
