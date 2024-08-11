from aiohttp import web

from db.queries import insert_measurements, select_measurements
from utils.constants import key_db_engine, key_valid_mtypes


class MeasurementsHandler:
    """Hanlder class containing functions to write and read measurement API calls."""

    async def write_measurement(self, request: web.Request) -> web.Response:
        """Handles request to write new measurement(s) to the database.

        Args:
            request (web.Request): Request containing measurement_type in match_info and values
                to be written into the database.

        Returns:
            web.Response: 204 if the values were written successfully, 400 if unsupported
                measurement_type was provided, 500 in case of any other error.
        """
        mtype = request.match_info["measurement_type"]

        if mtype not in request.app[key_valid_mtypes]:
            return web.HTTPBadRequest(text=f"Measurement type '{mtype}' not supported.")

        db_engine = request.app[key_db_engine]

        try:
            data = await request.json()
            await insert_measurements(engine=db_engine, data=data["values"], type=mtype)
        except Exception as e:
            return web.HTTPInternalServerError(text=repr(e))

        return web.HTTPNoContent()

    async def read_measurements(self, request: web.Request) -> web.Response:
        """Handles request to read measurement(s) from the database.

        Args:
            request (web.Request): Request containing measurement, from_time, and to_time values.

        Returns:
            web.Response: 200 containing measurements if values were retrieved successfully,
                400 if measurement, from_time, or to_time were missing in the query params,
                500 in case of any other error.
        """
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
