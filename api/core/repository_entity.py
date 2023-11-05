from sqlalchemy import select, insert, or_
from game import models, schemas
from datetime import datetime
from sqlalchemy.sql import func
from typing import Union


class Base:
    def __init__(self, session):
        self.session = session

    @staticmethod
    async def _all(result):
        row = result.all()
        return [data[0] for data in row]

    @staticmethod
    def _first(result):
        result = result.first()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def _one(result):
        return result.one()

    @staticmethod
    def _count(result):
        return len(result)

    async def _add(self, obj, data):
        data = data.dict()
        query = insert(obj).values(**data)
        await self.session.execute(query)
        await self.session.commit()
        return {
            "status": "success"
        }

    async def _update(self, obj, data):
        for field, value in data.dict().items():
            setattr(obj, field, value)
        await self.session.commit()
        return {
            "status": "success"
        }

    async def _delete(self, obj):
        await self.session.delete(obj)
        await self.session.commit()
        return {
            "status": "success"
        }


class PlayerEntity(Base):
    ...


class CurrencyEntity(Base):
    ...


class BalanceEntity(Base):
    ...


class HomeEntity(Base):
    ...


class SkillEntity(Base):
    ...


class TransportEntity(Base):
    ...


class StreetActionEntity(Base):
    ...


class WorkEntity(Base):
    ...


class FoodEntity(Base):
    ...


class HealthEntity(Base):
    ...


class LeisureEntity(Base):
    ...


class BusinessEntity(Base):
    ...

