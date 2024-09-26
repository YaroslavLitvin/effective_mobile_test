from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    model_validator
)

from app.schemas.base import (
    PaginationBase,
    IdFieldMixin
)


class S_Product(BaseModel):
    name: str
    description: Optional[str] = Field(None, examples=['Description', None])
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)


class S_ProductInput(IdFieldMixin):
    quantity: int


class S_ProductOptional(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)

    @model_validator(mode='after')
    def validate(self):
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("All fields are null")
        return self


class S_ProductFull(S_Product, IdFieldMixin):
    pass


class S_ProductPagination(PaginationBase[S_ProductFull]):
    pass
