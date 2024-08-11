from aiohttp import web


class IndexHandler:
    """Hanlder class containing functions to index and index-like routes within API."""

    async def index(self, request: web.Request) -> web.Response:
        """Dummy function to test API availability.

        Args:
            request (web.Request): API Request.

        Returns:
            web.Response: Response with 200 OK response status and text "Index".
        """
        return web.Response(text="Index")
