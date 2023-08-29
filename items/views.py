from fastapi import APIRouter, Body, Depends, Path
from typing import Annotated
from sqlalchemy.orm import Session

from test_app.database import get_db
from test_app.dependencies import get_current_user_id

from .schemas import ItemSchema, ItemIDSchema, ItemUpdateSchema, ItemSchemaWithID
from .helpers import ItemHandler

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.post("/", response_model=ItemIDSchema)
async def create_item(
    item_data: Annotated[ItemSchema, Body(title="Item to be created")],
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    handler_obj = ItemHandler(db=db, user_id=user_id)
    item = await handler_obj.create(item_data)
    return item


@router.get("/", response_model=list[ItemSchemaWithID])
async def fetch_item_list(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    handler_obj = ItemHandler(db=db, user_id=user_id)
    return await handler_obj.list()


@router.get("/{item_id}", response_model=ItemSchema)
async def fetch_item(
    item_id: Annotated[int, Path(title="ID of the item to be fetched")],
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    handler_obj = ItemHandler(db=db, user_id=user_id)
    item = await handler_obj.get(item_id)
    return item


@router.put("/{item_id}", response_model=ItemIDSchema)
async def update_item(
    item_id: Annotated[int, Path(title="ID of the item to be updated")],
    item_data: Annotated[ItemUpdateSchema, Body(title="Item data to be updated")],
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    handler_obj = ItemHandler(db=db, user_id=user_id)
    item = await handler_obj.update(item_id, item_data)
    return item


@router.delete("/{item_id}", response_model=ItemIDSchema)
async def delete_item(
    item_id: Annotated[int, Path(title="ID of the item to be deleted")],
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    handler_obj = ItemHandler(db=db, user_id=user_id)
    deleted_item = await handler_obj.delete(item_id)
    return deleted_item
