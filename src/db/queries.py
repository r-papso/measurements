import time
from typing import List

from sqlalchemy import and_, func, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine

from db.models import measurement_table


async def insert_measurement(engine: AsyncEngine, data: List[dict], type: str) -> None:
    async with engine.begin() as conn:
        val_dict = [
            {"time": val["time"], "value": val["value"], "type": type, "created_at": time.time()}
            for val in data
        ]
        _ = await conn.execute(insert(measurement_table, val_dict))


async def select_measurements(
    engine: AsyncEngine, time_from: int, time_to: int, type: str
) -> List[dict]:
    async with engine.connect() as conn:
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

        ranked = select(
            filtered.c.time,
            filtered.c.value,
            filtered.c.created_at,
            func.rank()
            .over(partition_by=filtered.c.time, order_by=filtered.c.created_at.asc())
            .label("rank"),
        ).alias()

        query = select(ranked.c.time, ranked.c.value, ranked.c.rank, filtered.c.created_at).where(
            ranked.c.rank == 1
        )
        result = await conn.execute(query)

        return [dict(row) for row in result.mappings()]
