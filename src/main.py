import asyncio
import sys
from typing import List

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from api.index import IndexHandler
from api.measurements import MeasurementsHandler
from db.models import metadata_obj
from utils.constants import key_db_engine, key_valid_mtypes


async def init_app(valid_measurements: List[str]):
    """Initialize AIOHTTP application.

    Args:
        valid_measurements (List[str]): Valid measurement types.
    """
    app = web.Application()

    measurement_handler = MeasurementsHandler()
    index_handler = IndexHandler()

    app.add_routes(
        [
            web.get("/api/v1/measurements", measurement_handler.read_measurements),
            web.post(
                "/api/v1/measurements/{measurement_type}", measurement_handler.write_measurement
            ),
        ]
    )
    app.add_routes([web.get("/", index_handler.index)])

    app[key_valid_mtypes] = valid_measurements
    app[key_db_engine] = create_async_engine("sqlite+aiosqlite:///measurements.db", echo=True)

    # Create measurement table in DB, if not exist.
    async with app[key_db_engine].begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()

    # wait forever
    await asyncio.Event().wait()


if __name__ == "__main__":
    valid_mtypes = sys.argv[1:]
    asyncio.run(init_app(valid_mtypes))
