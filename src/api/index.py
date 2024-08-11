from aiohttp import web


class IndexHandler:
    async def index(self, request: web.Request) -> web.Response:
        return web.Response(text="Index")
