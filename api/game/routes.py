from config import logger
from core.engine import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from game import logic, schemas
from users.models import User
from users.utils import current_user


router = APIRouter()


@router.get("/test")
async def test() -> dict:
    """ Test endpoint
    """
    return {"test": "ok"}


@router.get("/info", response_model=schemas.PlayerSchema)
async def get_play_info(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> schemas.PlayerSchema | JSONResponse:
    """ Info endpoint
    """
    player = logic.Player(user=user, session=session)
    player_info = await player.get_info()
    if not player_info:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Player is not exist for user - {user.email}"}
        )
    return schemas.PlayerSchema.from_orm(player_info)


@router.post("/player")
async def add_player(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Add player
    """
    if len(user.players):
        error_message = f"Player already exists for user - {user.email}"
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": error_message}
        )

    player = logic.Player(user=user, session=session)
    await player.add_player()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Created"}
    )


@router.get("/skills")
async def get_skills_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Skills endpoint
    """
    return {"test": "ok"}


@router.post("/skills")
async def learn_skill(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Learn skill endpoint by player id
    """
    return {"test": "ok"}


@router.get("/homes")
async def get_homes_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Homes endpoint
    """
    return {"test": "ok"}


@router.post("/homes")
async def buy_home(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Buy home by player id endpoint
    """
    return {"test": "ok"}


@router.get("/transport")
async def get_transport_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Transport endpoint
    """
    return {"test": "ok"}


@router.post("/transport")
async def buy_transport(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Buy transport by player id endpoint
    """
    return {"test": "ok"}


@router.get("/street")
async def get_street_actions_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Street actions endpoint
    """
    return {"test": "ok"}


@router.post("/street")
async def perform_street_action(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Perform street action by player id endpoint
    """
    return {"test": "ok"}


@router.get("/work")
async def get_work_action_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Work actions endpoint
    """
    return {"test": "ok"}


@router.post("/work")
async def perform_work_action(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Perform work  action by player id endpoint
    """
    return {"test": "ok"}


@router.get("/food")
async def get_food_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Food endpoint
    """
    return {"test": "ok"}


@router.post("/food")
async def buy_food(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Buy food by player id endpoint
    """
    return {"test": "ok"}


@router.get("/health")
async def get_health_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Health endpoint
    """
    return {"test": "ok"}


@router.post("/health")
async def buy_health(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Buy health by player id endpoint
    """
    return {"test": "ok"}


@router.get("/leisure")
async def get_leisure_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Leisure endpoint
    """
    return {"test": "ok"}


@router.post("/leisure")
async def buy_leisure(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Buy leisure by player id endpoint
    """
    return {"test": "ok"}


@router.get("/business")
async def get_business_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Business endpoint
    """
    return {"test": "ok"}


@router.post("/business")
async def buy_business(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Buy business by player id endpoint
    """
    return {"test": "ok"}
