from test_app.database import Base

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.now)
    modified_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    items = relationship("Item", back_populates="owner")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.email}"
