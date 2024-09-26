from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    debug: bool

    app_name: str
    app_host: str
    app_port: int

    db_host: str = 'database'
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    def db_dsn(
        self,
        driver: str = 'asyncpg',
        host: Optional[str] = None,
        port: Optional[int] = None
    ) -> str:
        from sqlalchemy.engine.url import URL

        host = self.db_host if host is None else host
        port = self.db_port if port is None else port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.db_user,
            password=self.db_pass,
            host=host,
            port=port if port != 5432 else None,
            database=self.db_name,
        )
        dsn = uri.render_as_string(hide_password=False)
        # print('-------------------------------------------------')
        # print(f'{dsn=}')
        # print('-------------------------------------------------')
        return dsn

    class Config:
        validate_assignment = False


# Загружаем переменные из файла .env, если он существует
load_dotenv()


config = Config()
