from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from test_app.helpers import ModelHandler

from .models import Item
from .schemas import ItemSchema, ItemUpdateSchema, ItemIDSchema

import logging
logger = logging.getLogger(__name__)


class ItemHandler(ModelHandler):

    def __init__(self, db: AsyncSession, user_id: int) -> None:
        self.db = db
        self.user_id = user_id


    async def __fetch_item(self, item_id) -> Item:
        query = await self.db.execute(
            select(Item).filter(
                Item.id == item_id,
                Item.owner_id == self.user_id,
                Item.is_active == True
            )
        )
        item = query.scalar_one_or_none()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        return item


    async def create(self, item_data: ItemSchema) -> Item:
        item_obj = Item(**item_data.dict(), owner_id=self.user_id)
        self.db.add(item_obj)
        await self.db.commit()
        await self.db.refresh(item_obj)
        return item_obj


    async def list(self) -> list[Item]:
        query = await self.db.execute(
            select(Item).filter(
                Item.owner_id == self.user_id,
                Item.is_active == True
            )
        )
        item_data = query.scalars().all()
        if item_data:
            return [item for item in item_data]
        return []


    async def get(self, item_id) -> Item:
        return await self.__fetch_item(item_id)


    async def update(self, item_id, item_data: ItemUpdateSchema) -> Item:
        item_obj = await self.__fetch_item(item_id)
        item_dict = item_data.dict(exclude_unset=True)
        if 'id' in item_dict:
            del item_dict['id']
        for key, value in item_dict.items():
            setattr(item_obj, key, value)
        self.db.add(item_obj)
        await self.db.commit()
        await self.db.refresh(item_obj)
        return item_obj


    async def delete(self, item_id) -> ItemIDSchema:
        item_obj = await self.__fetch_item(item_id)
        item_obj.is_active = False
        self.db.add(item_obj)
        await self.db.commit()
        await self.db.refresh(item_obj)
        return item_obj
