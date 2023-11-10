from core.engine import async_session_maker
from datetime import datetime
from game import models, schemas
from sqlalchemy import select, insert


async def init_db() -> None:
    """ Initialisation empty db
    :return:
    """
    currency_list = ["bottle", "RUB", "USD", "BTC"]

    async with async_session_maker() as session:
        need_commit = False

        query = select(models.Currency)
        try:
            result = await session.execute(query)
        except Exception as e:
            print(e)
            return
        existing_currencies = result.all()

        currencies = []
        for item_currency_name in currency_list:
            currencies.append(
                models.Currency(name=item_currency_name)
            )

        if not len(existing_currencies):
            for currency in currencies:
                print(f"Add {currency}")
                session.add(currency)
                need_commit = True

        if need_commit:
            await session.commit()


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
        if not isinstance(data, dict):
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
    model = models.Player

    async def get_player_by_id(self, player_id: int) -> models.Player:
        query = select(self.model).filter(self.model.id == player_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreatePlayer | dict) -> int:
        query = select(models.Currency)
        result = await self.session.execute(query)
        all_currencies = [item[0] for item in result]

        if not isinstance(data, dict):
            data = data.dict()

        player = self.model(**data)
        self.session.add(player)
        await self.session.commit()

        if all_currencies and isinstance(all_currencies, list):
            for item_currency in all_currencies:
                balance_name = self.__map_balance_name(currency_name=item_currency.name)
                if not balance_name:
                    continue
                balance = models.Balance(
                    name=balance_name,
                    currency_id=item_currency.id,
                    player_id=player.id,
                    amount=0,
                    updated_at=datetime.now()
                )
                self.session.add(balance)

        await self.session.commit()
        return player.id

    @staticmethod
    def __map_balance_name(currency_name: str) -> str | None:
        balance_mapping = {
            "bottle": "Бутылки",
            "RUB": "Рубли",
            "USD": "Баксы",
            "BTC": "Биткоины"
        }
        return balance_mapping.get(currency_name, None)


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

