from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)


from app.configuration import Config


def create_engine(db: Config, echo: bool = False):
    engine = create_async_engine(
        db.db_dsn(),
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
    )
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
