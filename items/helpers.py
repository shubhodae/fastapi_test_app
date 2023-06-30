from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Item
from .schemas import ItemSchema, ItemUpdateSchema

import logging
logger = logging.getLogger(__name__)


class ItemHandler:

    def __init__(self, db: Session) -> None:
        self.db = db

    def __fetch_item(self, item_id) -> Item:
        item = self.db.query(Item).filter(
            Item.id == item_id
        ).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        return item

    def create(self, item_data: ItemSchema) -> Item:
        item_obj = Item(**item_data.dict())
        self.db.add(item_obj)
        self.db.commit()
        self.db.refresh(item_obj)
        return item_obj
    
    def get_list(self) -> list[Item]:
        item_query = self.db.query(Item).all()
        item_list = [item for item in item_query]
        return item_list
    
    def get(self, item_id) -> Item:
        return self.__fetch_item(item_id)
    
    def update(self, item_id, item_data: ItemUpdateSchema) -> Item:
        item_obj = self.__fetch_item(item_id)
        item_dict = item_data.dict(exclude_unset=True)
        if 'id' in item_dict:
            del item_dict['id']
        for key, value in item_dict.items():
            setattr(item_obj, key, value)
        self.db.add(item_obj)
        self.db.commit()
        self.db.refresh(item_obj)
        return item_obj
    
    def delete(self, item_id) -> int:
        item_obj = self.__fetch_item(item_id)
        self.db.delete(item_obj)
        self.db.commit()
        return item_id
