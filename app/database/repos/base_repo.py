from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    """
    A class representing a base repository for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.

    """

    def __init__(self, session):
        self.session: AsyncSession = session

    async def delete(
        self,
        id: int
    ) -> None:
        entry = await self.read(id)
        if entry is None:
            raise ValueError("Entry not found")
        await self.session.delete(entry)
        await self.session.commit()
