from fastapi import APIRouter
from game import routes as game_endpoints


routes = APIRouter()

routes.include_router(
    game_endpoints.router,
    prefix="/api",
    tags=["finance"]
)
