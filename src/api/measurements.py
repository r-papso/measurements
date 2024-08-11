import time
from aiohttp import web

from db.queries import insert_measurement, select_measurements
from utils.constants import key_db_engine, key_valid_mtypes


class MeasurementsHandler:
    async def write_measurement(self, request: web.Request) -> web.Response:
        mtype = request.match_info["measurement_type"]

        if mtype not in request.app[key_valid_mtypes]:
            return web.HTTPBadRequest(text=f"Measurement type '{mtype}' not supported.")

        db_engine = request.app[key_db_engine]

        try:
            data = await request.json()
            created_at = time.time()

            await insert_measurement(
                engine=db_engine,
                time=data["time"],
                value=data["value"],
                type=mtype,
                created_at=created_at,
            )
        except Exception as e:
            return web.HTTPInternalServerError(text=repr(e))

        return web.HTTPNoContent()

    async def read_measurements(self, request: web.Request) -> web.Response:
        params = request.rel_url.query

        if "measurement" not in params:
            return web.HTTPBadRequest(text="Query missing argument: measurement")

        if "from_time" not in params:
            return web.HTTPBadRequest(text="Query missing argument: from_time")

        if "to_time" not in params:
            return web.HTTPBadRequest(text="Query missing argument: to_time")

        response_data = {}
        db_engine = request.app[key_db_engine]

        try:
            for mtype in params.getall("measurement"):
                response_data[mtype] = await select_measurements(
                    engine=db_engine,
                    time_from=params["from_time"],
                    time_to=params["to_time"],
                    type=mtype,
                )
        except Exception as e:
            return web.HTTPInternalServerError(text=repr(e))

        return web.json_response(response_data)
