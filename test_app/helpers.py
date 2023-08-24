from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import List

from sqlalchemy.orm import Session


# Handler Interface
class ModelHandler(ABC):

    @abstractmethod
    def __init__(self, db: Session, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def create(self, schema: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    def update(self, obj_id: int, schema: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    def get(self, obj_id: int) -> BaseModel:
        pass

    @abstractmethod
    def list(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def delete(self, obj_id: int) -> BaseModel:
        pass
