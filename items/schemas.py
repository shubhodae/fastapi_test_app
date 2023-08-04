from pydantic import BaseModel, Field

from .models import ItemType


class ItemSchema(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    category: str | None = None
    item_type: ItemType = ItemType.type_1

    class Config:
        orm_mode = True


class ItemIDSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ItemSchemaWithID(ItemSchema, ItemIDSchema):
    pass


class ItemUpdateSchema(BaseModel):
    name: str | None = Field(min_length=1, max_length=128, default=None)
    category: str | None
    item_type: ItemType | None

    class Config:
        orm_mode = True
