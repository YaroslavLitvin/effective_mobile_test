from datetime import datetime
from typing import List, TypeVar, Generic

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class PaginationBase(BaseModel, Generic[T]):
    items: List[T]
    current_page: int
    last_page: int
    total: int


class IdFieldMixin(BaseModel):
    id: int


class TimestampFieldMixin(BaseModel):
    created_at: datetime
