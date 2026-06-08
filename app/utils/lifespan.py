from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import db 

@asynccontextmanager
async def on_startup(app: FastAPI):
    await db.create_all_tables()
    yield