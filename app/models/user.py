from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String

from app.db.base_class import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    full_name = Column(String, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_superuser = Column(Boolean(), nullable=False, server_default="false")
