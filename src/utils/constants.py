from typing import List

from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncEngine

key_valid_mtypes = web.AppKey("valid_measurements", List[str])
key_db_engine = web.AppKey("db_engine", AsyncEngine)
