from pydantic import BaseModel

from .models import ItemType


class ItemSchema(BaseModel):
    id: int
    name: str
    category: str | None = None
    item_type: ItemType = ItemType.type_1
    is_active: bool = True
    owner_id: int

    class Config:
        orm_mode = True


class ItemIDSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ItemUpdateSchema(BaseModel):
    name: str | None
    category: str | None
    item_type: ItemType | None
    is_active: bool | None
    owner_id: int | None

    class Config:
        orm_mode = True
