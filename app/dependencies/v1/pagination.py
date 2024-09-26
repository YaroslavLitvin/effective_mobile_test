from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class Paginator(BaseModel):
    page: int = Field(1, ge=1)
    items_on_page: int = Field(1, ge=1, le=100)


D_PaginationParams = Annotated[Paginator, Depends()]
