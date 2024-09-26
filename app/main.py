import uvicorn
from fastapi import FastAPI


from .routers.router import router
from .configuration import config
from .version import VERSION
from .logging_setup import setup_logging


app = FastAPI(
    debug=config.debug,
    version=VERSION,
    title='Test Task',
    docs_url="/docs" if config.debug else None,
)
app.include_router(router)


if __name__ == "__main__":
    setup_logging()
    uvicorn.run(app, host=config.app_host, port=config.app_port)
