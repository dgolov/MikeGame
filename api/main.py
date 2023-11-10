import asyncio

from config import logger
from core.repository_entity import init_db
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from routes import routes


app = FastAPI()


app.include_router(routes)
logger.debug("Start application")

loop = asyncio.get_running_loop()
loop.create_task(init_db())


@app.middleware("http")
async def exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        logger.debug(
            f"{request.scope['client'][0]}: {request.scope['client'][1]} - '{request.method} {request.scope['path']} "
            f"{request.scope['scheme']}/{request.scope['http_version']} {response.status_code}'"
        )
        return response
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
