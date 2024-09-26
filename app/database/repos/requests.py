from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

# from .example_repo import ExampleRepo
from .order import OrdersRepo
from .product import ProductsRepo
from .order_item import OrderItemsRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations.
    This class holds all the repositories for the database models.

    You can add more repositories as properties to this class,
    so they will be easily accessible.
    """

    session: AsyncSession

    # @property
    # def example(self) -> ExampleRepo:
    #     return ExampleRepo(self.session)

    @property
    def orders(self) -> OrdersRepo:
        return OrdersRepo(self.session)

    @property
    def order_items(self) -> OrderItemsRepo:
        return OrderItemsRepo(self.session)

    @property
    def products(self) -> ProductsRepo:
        return ProductsRepo(self.session)
