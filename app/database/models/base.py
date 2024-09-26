from datetime import datetime
from abc import abstractmethod
from typing import Any, Dict, TypeVar, Generic

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func

from pydantic import BaseModel


V = TypeVar("V", bound=BaseModel)


class Base(DeclarativeBase):

    def _class_name(self) -> str:
        return self.__class__.__name__


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        class_name = cls.__name__.lower()
        return class_name + f"{'es' if class_name[-1]=='s' else 's'}"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )


class ToSchemaMixin(Generic[V]):

    @abstractmethod
    def to_schema(self) -> V:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return (self.to_schema()).model_dump()

    def to_json(self) -> str:
        return (self.to_schema()).model_dump_json()
