from test_app.database import Base, BaseModel

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

import enum


class ItemType(str, enum.Enum):
    type_1 = "Type 1"
    type_2 = "Type 2"
    type_3 = "Type 3"


class Item(Base, BaseModel):
    __tablename__ = "items"

    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)
    item_type = Column(Enum(ItemType), default=ItemType.type_1)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    def __str__(self):
        return f"{self.id} - {self.name}"
