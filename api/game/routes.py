import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import Union, List


router = APIRouter()


@router.get("/test")
async def test() -> dict:
    """ Test endpoint
    """
    return {"test": "ok"}


@router.get("/info")
async def get_play_info() -> dict:
    """ Info endpoint
    """
    return {"test": "ok"}


@router.get("/skills")
async def get_skills_list() -> dict:
    """ Skills endpoint
    """
    return {"test": "ok"}


@router.post("/skills")
async def learn_skill() -> dict:
    """ Learn skill endpoint by player id
    """
    return {"test": "ok"}


@router.get("/homes")
async def get_homes_list() -> dict:
    """ Homes endpoint
    """
    return {"test": "ok"}


@router.post("/homes")
async def buy_home() -> dict:
    """ Buy home by player id endpoint
    """
    return {"test": "ok"}


@router.get("/transport")
async def get_transport_list() -> dict:
    """ Transport endpoint
    """
    return {"test": "ok"}


@router.post("/transport")
async def buy_transport() -> dict:
    """ Buy transport by player id endpoint
    """
    return {"test": "ok"}


@router.get("/street")
async def get_street_actions_list() -> dict:
    """ Street actions endpoint
    """
    return {"test": "ok"}


@router.post("/street")
async def perform_street_action() -> dict:
    """ Perform street action by player id endpoint
    """
    return {"test": "ok"}


@router.get("/work")
async def get_work_action_list() -> dict:
    """ Work actions endpoint
    """
    return {"test": "ok"}


@router.post("/work")
async def perform_work_action() -> dict:
    """ Perform work  action by player id endpoint
    """
    return {"test": "ok"}


@router.get("/food")
async def get_food_list() -> dict:
    """ Food endpoint
    """
    return {"test": "ok"}


@router.post("/food")
async def buy_food() -> dict:
    """ Buy food by player id endpoint
    """
    return {"test": "ok"}


@router.get("/health")
async def get_health_list() -> dict:
    """ Health endpoint
    """
    return {"test": "ok"}


@router.post("/health")
async def buy_health() -> dict:
    """ Buy health by player id endpoint
    """
    return {"test": "ok"}


@router.get("/leisure")
async def get_leisure_list() -> dict:
    """ Leisure endpoint
    """
    return {"test": "ok"}


@router.post("/leisure")
async def buy_leisure() -> dict:
    """ Buy leisure by player id endpoint
    """
    return {"test": "ok"}


@router.get("/business")
async def get_business_list() -> dict:
    """ Business endpoint
    """
    return {"test": "ok"}


@router.post("/business")
async def buy_business() -> dict:
    """ Buy business by player id endpoint
    """
    return {"test": "ok"}
