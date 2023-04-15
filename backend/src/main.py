import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine

from .config import settings
from .routers import api
from .utils import get_connection_url, wait_for_db, write_data_to_db

FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api.router)

# Add CORS middleware with allowed origins set to the frontend container's IP address
# FIXME Could be resolved with ngnix
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{settings.FE_HOST}", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    engine = create_engine(get_connection_url(settings))
    wait_for_db(engine)
    write_data_to_db(
        engine,
        settings.DATA_SOURCE,
        settings.raw_table_name,
        settings.heatmap_table_name,
    )


@app.get("/")
async def root():
    return {"message": "Hello world"}
