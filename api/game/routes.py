from config import logger
from core.engine import get_async_session
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from game import logic, schemas, services
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
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


@router.get("/skills", response_model=List[schemas.SkillSchema])
async def get_skills_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.SkillSchema]:
    """ Skills endpoint
    """
    skill_logic = logic.Skill(session=session, user=user)
    skills = await skill_logic.get_skill_list()
    return [
        schemas.SkillSchema.from_orm(item_skill) for item_skill in skills
    ]


@router.post("/skills")
async def learn_skill(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Learn skill endpoint by player id
    """
    skill_logic = logic.Skill(session=session, user=user)
    return await services.processing_by_item_request(game_logic=skill_logic, data=data)


@router.get("/homes", response_model=List[schemas.HomeSchema])
async def get_homes_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.HomeSchema]:
    """ Homes endpoint
    """
    home_logic = logic.Home(session=session, user=user)
    home_list = await home_logic.get_home_list()
    return [
        schemas.HomeSchema.from_orm(home) for home in home_list
    ]


@router.post("/homes")
async def buy_home(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Buy home by player id endpoint
    """
    home_logic = logic.Home(session=session, user=user)
    return await services.processing_by_item_request(game_logic=home_logic, data=data)


@router.get("/transport", response_model=List[schemas.TransportSchema])
async def get_transport_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.TransportSchema]:
    """ Transport endpoint
    """
    transport_logic = logic.Transport(session=session, user=user)
    transport_list = await transport_logic.get_transport_list()
    return [
        schemas.TransportSchema.from_orm(transport) for transport in transport_list
    ]


@router.post("/transport")
async def buy_transport(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Buy transport by player id endpoint
    """
    transport_logic = logic.Transport(session=session, user=user)
    return await services.processing_by_item_request(game_logic=transport_logic, data=data)


@router.get("/street", response_model=List[schemas.StreetActionSchema])
async def get_street_actions_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.StreetActionSchema]:
    """ Street actions endpoint
    """
    street_logic = logic.StreetAction(session=session, user=user)
    street_action_list = await street_logic.get_street_action_list()
    return [
        schemas.StreetActionSchema.from_orm(action) for action in street_action_list
    ]


@router.post("/street")
async def perform_street_action(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """ Perform street action by player id endpoint
    """
    street_logic = logic.StreetAction(session=session, user=user)
    await services.processing_action_request(game_logic=street_logic, data=data)


@router.get("/work", response_model=List[schemas.WorkSchema])
async def get_work_action_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.WorkSchema]:
    """ Work actions endpoint
    """
    work_logic = logic.Work(session=session, user=user)
    work_list = await work_logic.get_work_list()
    return [
        schemas.WorkSchema.from_orm(work) for work in work_list
    ]


@router.post("/work")
async def perform_work_action(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Perform work action by player id endpoint
    """
    work_logic = logic.Work(session=session, user=user)
    return await services.processing_action_request(game_logic=work_logic, data=data)


@router.get("/food", response_model=List[schemas.FoodSchema])
async def get_food_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.FoodSchema]:
    """ Food endpoint
    """
    food_logic = logic.Food(session=session, user=user)
    food_list = await food_logic.get_food_list()
    return [
        schemas.FoodSchema.from_orm(food) for food in food_list
    ]


@router.post("/food")
async def buy_food(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Buy food by player id endpoint
    """
    food_logic = logic.Food(session=session, user=user)
    return await services.processing_buy_services_request(game_logic=food_logic, data=data)


@router.get("/health", response_model=List[schemas.HealthSchema])
async def get_health_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.HealthSchema]:
    """ Health endpoint
    """
    health_logic = logic.Health(session=session, user=user)
    health_list = await health_logic.get_health_list()
    return [
        schemas.HealthSchema.from_orm(health) for health in health_list
    ]


@router.post("/health")
async def buy_health(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Buy health by player id endpoint
    """
    health_logic = logic.Health(session=session, user=user)
    return await services.processing_buy_services_request(game_logic=health_logic, data=data)


@router.get("/leisure", response_model=List[schemas.LeisureSchema])
async def get_leisure_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.LeisureSchema]:
    """ Leisure endpoint
    """
    leisure_logic = logic.Leisure(session=session, user=user)
    leisure_list = await leisure_logic.get_leisure_list()
    return [
        schemas.LeisureSchema.from_orm(leisure) for leisure in leisure_list
    ]


@router.post("/leisure")
async def buy_leisure(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Buy leisure by player id endpoint
    """
    leisure_logic = logic.Leisure(session=session, user=user)
    return await services.processing_buy_services_request(game_logic=leisure_logic, data=data)


@router.get("/business", response_model=List[schemas.BusinessSchema])
async def get_business_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.BusinessSchema]:
    """ Business endpoint
    """
    business_logic = logic.Business(session=session, user=user)
    business_list = await business_logic.get_business_list()
    return [
        schemas.BusinessSchema.from_orm(business) for business in business_list
    ]


@router.post("/business")
async def buy_business(
        data: schemas.PerformActionSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """ Buy business by player id endpoint
    """
    business_logic = logic.Business(session=session, user=user)
    return await services.processing_by_item_request(game_logic=business_logic, data=data)
