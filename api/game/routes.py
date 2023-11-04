import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import Union, List


router = APIRouter()


@router.get("/test")
async def main() -> dict:
    """ Main endpoint
    """
    return {"test": "ok"}
