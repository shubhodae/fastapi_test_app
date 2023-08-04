from test_app.database import Base, BaseModel

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship



class User(Base, BaseModel):
    __tablename__ = "users"

    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.email}"
