from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from altlinker.telegram_handler import update_data_handler


async def check(request) -> dict:
    return JSONResponse({"message": "OK!"})


async def telegram_handler(request: Request) -> JSONResponse:
    data = await request.json()
    await update_data_handler(data)
    return JSONResponse({"message": "OK!"})


routes = [
    Route("/check", endpoint=check),
    Route("/telegram/hook", endpoint=telegram_handler, methods=["POST"]),
]


app = Starlette(routes=routes)
