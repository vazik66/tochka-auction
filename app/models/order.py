from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID


class Order(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    item_id = Column(UUID(as_uuid=True), ForeignKey("item.id"))
    amount = Column(
        Integer,
        nullable=False,
    )
    status = Column(Integer, nullable=False)
