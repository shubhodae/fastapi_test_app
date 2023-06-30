from test_app.database import Base

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

import enum
from datetime import datetime


class ItemType(str, enum.Enum):
    type_1 = "Type 1"
    type_2 = "Type 2"
    type_3 = "type_3"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)
    item_type = Column(Enum(ItemType), default=ItemType.type_1)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.now)
    modified_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner = relationship("User", back_populates="items")

    def __str__(self):
        return f"{self.id} - {self.name}"
