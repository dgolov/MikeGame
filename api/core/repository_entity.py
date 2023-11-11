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
    def _all(result):
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
    model = models.Currency

    async def get_currency_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_currency_by_id(self, currency_id: int) -> models.Currency:
        query = select(self.model).filter(self.model.id == currency_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateCurrency | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        currency = self.model(**data)
        self.session.add(currency)
        await self.session.commit()
        return currency.id

    async def update(self, currency_id: int, data: schemas.UpdateCurrency):
        currency = await self.session.get(self.model, currency_id)
        if not currency:
            return {
                "status": "fail",
                "message": "Currency is not found"
            }
        return await self._update(currency, data)

    async def delete(self, currency_id: int):
        currency = await self.session.get(self.model, currency_id)
        if not currency:
            return {
                "status": "fail",
                "message": "Currency is not found"
            }
        return await self._delete(currency)


class BalanceEntity(Base):
    model = models.Balance

    async def get_balance_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_balance_by_id(self, balance_id: int) -> models.Balance:
        query = select(self.model).filter(self.model.id == balance_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateBalance | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        balance = self.model(**data)
        self.session.add(balance)
        await self.session.commit()
        return balance.id

    async def update(self, balance_id: int, data: schemas.UpdateBalance):
        balance = await self.session.get(self.model, balance_id)
        if not balance:
            return {
                "status": "fail",
                "message": "Balance is not found"
            }
        return await self._update(balance, data)

    async def delete(self, balance_id: int):
        balance = await self.session.get(self.model, balance_id)
        if not balance:
            return {
                "status": "fail",
                "message": "Balance is not found"
            }
        return await self._delete(balance)


class HomeEntity(Base):
    model = models.Home

    async def get_home_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_home_by_id(self, home_id: int) -> models.Home:
        query = select(self.model).filter(self.model.id == home_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateHome | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        home = self.model(**data)
        self.session.add(home)
        await self.session.commit()
        return home.id

    async def update(self, home_id: int, data: schemas.UpdateHome):
        home = await self.session.get(self.model, home_id)
        if not home:
            return {
                "status": "fail",
                "message": "Home is not found"
            }
        return await self._update(home, data)

    async def delete(self, home_id: int):
        home = await self.session.get(self.model, home_id)
        if not home:
            return {
                "status": "fail",
                "message": "Home is not found"
            }
        return await self._delete(home)


class SkillEntity(Base):
    model = models.Skill

    async def get_skill_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_skill_by_id(self, skill_id: int) -> models.Skill:
        query = select(self.model).filter(self.model.id == skill_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateSkill | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        balance = self.model(**data)
        self.session.add(balance)
        await self.session.commit()
        return balance.id

    async def update(self, skill_id: int, data: schemas.UpdateSkill):
        skill = await self.session.get(self.model, skill_id)
        if not skill:
            return {
                "status": "fail",
                "message": "Skill is not found"
            }
        return await self._update(skill, data)

    async def delete(self, skill_id: int):
        skill = await self.session.get(self.model, skill_id)
        if not skill:
            return {
                "status": "fail",
                "message": "Skill is not found"
            }
        return await self._delete(skill)


class TransportEntity(Base):
    model = models.Transport

    async def get_transport_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_transport_by_id(self, transport_id: int) -> models.Transport:
        query = select(self.model).filter(self.model.id == transport_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateCurrency | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        transport = self.model(**data)
        self.session.add(transport)
        await self.session.commit()
        return transport.id

    async def update(self, transport_id: int, data: schemas.UpdateTransport):
        transport = await self.session.get(self.model, transport_id)
        if not transport:
            return {
                "status": "fail",
                "message": "Transport is not found"
            }
        return await self._update(transport, data)

    async def delete(self, transport_id: int):
        transport = await self.session.get(self.model, transport_id)
        if not transport:
            return {
                "status": "fail",
                "message": "Transport is not found"
            }
        return await self._delete(transport)


class StreetActionEntity(Base):
    model = models.StreetAction

    async def get_street_action_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_street_action_by_id(self, street_action_id: int) -> models.StreetAction:
        query = select(self.model).filter(self.model.id == street_action_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateStreetAction | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        street_action = self.model(**data)
        self.session.add(street_action)
        await self.session.commit()
        return street_action.id

    async def update(self, street_action_id: int, data: schemas.UpdateStreetAction):
        street_action = await self.session.get(self.model, street_action_id)
        if not street_action:
            return {
                "status": "fail",
                "message": "Street action is not found"
            }
        return await self._update(street_action, data)

    async def delete(self, street_action_id: int):
        street_action = await self.session.get(self.model, street_action_id)
        if not street_action:
            return {
                "status": "fail",
                "message": "Street action is not found"
            }
        return await self._delete(street_action)


class WorkEntity(Base):
    model = models.Work

    async def get_work_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_work_by_id(self, work_id: int) -> models.Work:
        query = select(self.model).filter(self.model.id == work_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateWork | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        work = self.model(**data)
        self.session.add(work)
        await self.session.commit()
        return work.id

    async def update(self, work_id: int, data: schemas.UpdateWork):
        work = await self.session.get(self.model, work_id)
        if not work:
            return {
                "status": "fail",
                "message": "Work is not found"
            }
        return await self._update(work, data)

    async def delete(self, work_id: int):
        work = await self.session.get(self.model, work_id)
        if not work:
            return {
                "status": "fail",
                "message": "Work is not found"
            }
        return await self._delete(work)


class FoodEntity(Base):
    model = models.Food

    async def get_food_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_food_by_id(self, food_id: int) -> models.Food:
        query = select(self.model).filter(self.model.id == food_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateFood | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        food = self.model(**data)
        self.session.add(food)
        await self.session.commit()
        return food.id

    async def update(self, food_id: int, data: schemas.UpdateFood):
        food = await self.session.get(self.model, food_id)
        if not food:
            return {
                "status": "fail",
                "message": "Food is not found"
            }
        return await self._update(food, data)

    async def delete(self, food_id: int):
        food = await self.session.get(self.model, food_id)
        if not food:
            return {
                "status": "fail",
                "message": "Food is not found"
            }
        return await self._delete(food)


class HealthEntity(Base):
    model = models.Health

    async def get_health_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_health_by_id(self, health_id: int) -> models.Health:
        query = select(self.model).filter(self.model.id == health_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateHealth | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        health = self.model(**data)
        self.session.add(health)
        await self.session.commit()
        return health.id

    async def update(self, health_id: int, data: schemas.UpdateHealth):
        health = await self.session.get(self.model, health_id)
        if not health:
            return {
                "status": "fail",
                "message": "Health is not found"
            }
        return await self._update(health, data)

    async def delete(self, health_id: int):
        health = await self.session.get(self.model, health_id)
        if not health:
            return {
                "status": "fail",
                "message": "Health is not found"
            }
        return await self._delete(health)


class LeisureEntity(Base):
    model = models.Leisure

    async def get_leisure_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_leisure_by_id(self, leisure_id: int) -> models.Leisure:
        query = select(self.model).filter(self.model.id == leisure_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateLeisure | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        leisure = self.model(**data)
        self.session.add(leisure)
        await self.session.commit()
        return leisure.id

    async def update(self, leisure_id: int, data: schemas.UpdateLeisure):
        leisure = await self.session.get(self.model, leisure_id)
        if not leisure:
            return {
                "status": "fail",
                "message": "Leisure is not found"
            }
        return await self._update(leisure, data)

    async def delete(self, leisure_id: int):
        leisure = await self.session.get(self.model, leisure_id)
        if not leisure:
            return {
                "status": "fail",
                "message": "Leisure is not found"
            }
        return await self._delete(leisure)


class BusinessEntity(Base):
    model = models.Business

    async def get_business_list(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self._all(result)

    async def get_business_by_id(self, business_id: int) -> models.Business:
        query = select(self.model).filter(self.model.id == business_id)
        result = await self.session.execute(query)
        return self._first(result)

    async def create(self, data: schemas.CreateBusiness | dict) -> int:
        if not isinstance(data, dict):
            data = data.dict()

        business = self.model(**data)
        self.session.add(business)
        await self.session.commit()
        return business.id

    async def update(self, business_id: int, data: schemas.UpdateBusiness):
        business = await self.session.get(self.model, business_id)
        if not business:
            return {
                "status": "fail",
                "message": "Business is not found"
            }
        return await self._update(business, data)

    async def delete(self, business_id: int):
        business = await self.session.get(self.model, business_id)
        if not business:
            return {
                "status": "fail",
                "message": "Business is not found"
            }
        return await self._delete(business)
