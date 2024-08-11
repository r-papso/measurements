import time
from typing import List

from sqlalchemy import and_, func, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine

from db.models import measurement_table


async def insert_measurements(engine: AsyncEngine, data: List[dict], type: str) -> None:
    """Perform INSERT command to insert new measurements to the database.

    Args:
        engine (AsyncEngine): SQLAlchemy DB engine.
        data (List[dict]): Measurement data to be inserted.
        type (str): Measurement type.
    """
    async with engine.begin() as conn:
        val_dict = [
            {"time": val["time"], "value": val["value"], "type": type, "created_at": time.time()}
            for val in data
        ]
        _ = await conn.execute(insert(measurement_table, val_dict))


async def select_measurements(
    engine: AsyncEngine, time_from: int, time_to: int, type: str
) -> List[dict]:
    """Performs SELECT command to retrieve measurements from the database.

    Args:
        engine (AsyncEngine): SQLAlchemy DB engine.
        time_from (int): Start of the time interval.
        time_to (int): End of the time interval.
        type (str): Measurement type.

    Returns:
        List[dict]: Found measurements.
    """
    async with engine.connect() as conn:
        # First filter only rows of specified measurement type and within the time interval.
        filtered = (
            select(measurement_table)
            .where(
                and_(
                    measurement_table.c.type == type,
                    measurement_table.c.time >= time_from,
                    measurement_table.c.time < time_to,
                )
            )
            .alias()
        )

        # Next, as we're not having any constraints on the table - in order to maximize write
        # throughput - we need to drop duplicates. For each timestamp, we order all records by
        # created_at timestamp.
        ranked = select(
            filtered.c.time,
            filtered.c.value,
            filtered.c.created_at,
            func.row_number()
            .over(partition_by=filtered.c.time, order_by=filtered.c.created_at.asc())
            .label("rn"),
        ).alias()

        # Finally, for each partition, we select rows that have minimal created_at timestamp.
        query = select(ranked.c.time, ranked.c.value).where(ranked.c.rn == 1)
        result = await conn.execute(query)

        return [dict(row) for row in result.mappings()]
