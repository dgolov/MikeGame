from core import repository_entity
from config import logger
from game import models
from game.exceptions import NotFoundException, PlayerException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from users.models import User

import random


class Game:

    @staticmethod
    def get_current_player(func):
        def wrapper(self, *args, **kwargs):
            self.player = self.get_player()
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    def __init__(self, session: AsyncSession, user: User):
        self.session = session
        self.user = user
        self.player = None

    def next_day(self) -> None:
        logger.debug(f"{self.user.email} Set next day")
        self.player.day += 1
        self.session.add(self.player)

    def get_player(self) -> models.Player | None:
        try:
            return self.user.players[-1]
        except IndexError:
            logger.error(f"Player is not exist for user - {self.user.email}")

    def set_player_harm(
            self,
            harm_action: models.StreetAction | models.Work
    ) -> None:
        """ Set harm for player
        :param harm_action: harm action
        :return:
        """
        hunger_harm = self._get_random_value(
            min_value=harm_action.hunger_harm_min,
            max_value=harm_action.hunger_harm_max
        )
        rest_harm = self._get_random_value(
            min_value=harm_action.rest_harm_min,
            max_value=harm_action.rest_harm_max
        )
        health_harm = self._get_random_value(
            min_value=harm_action.health_harm_min,
            max_value=harm_action.health_harm_max
        )

        self.player.hunger -= hunger_harm
        self.player.rest -= rest_harm
        self.player.health -= health_harm
        self.session.add(self.player)

    def update_balance(
            self,
            action: models.StreetAction | models.Work
    ) -> None:
        """ Updated player balance after work or street action
        :param action: work or street action
        :return:
        """
        income = self._get_random_value(
            min_value=action.income_min,
            max_value=action.income_max
        )
        for balance in self.player.balances:
            if balance.currency.id == action.currency_id:
                balance.amount += income
                self.session.add(balance)

    @staticmethod
    def _get_random_value(min_value: int, max_value: int) -> int:
        return random.randint(min_value, max_value)


class Player(Game):
    def __init__(self, session: AsyncSession, user: User):
        self.default_player_data = {
            "hunger": 100,
            "rest": 100,
            "health": 100,
            "level": 1,
            "age": 18,
            "authority": 0,
            "day": 1,
            "user_id": None
        }
        super(Player, self).__init__(session, user)
        self.repository = repository_entity.PlayerEntity(session=session)

    async def add_player(self) -> None:
        self.default_player_data["user_id"] = self.user.id
        player_id = await self.repository.create(
            data=self.default_player_data
        )
        logger.info(
            f"[Logic.Player] Add new player (id - {player_id}) by user id - {self.user.id}"
        )

    async def get_info(self) -> models.Player | None:
        return self.get_player()


class Home(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Home, self).__init__(session, user)
        self.repository = repository_entity.HomeEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_home_list(self) -> List[models.Home]:
        return await self.repository.get_home_list()


class Skill(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Skill, self).__init__(session, user)
        self.repository = repository_entity.SkillEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_skill_list(self) -> List[models.Skill]:
        return await self.repository.get_skill_list()


class Transport(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Transport, self).__init__(session, user)
        self.repository = repository_entity.TransportEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_transport_list(self) -> List[models.Transport]:
        return await self.repository.get_transport_list()


class StreetAction(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(StreetAction, self).__init__(session, user)
        self.repository = repository_entity.StreetActionEntity(session=session)

    async def get_action(self, action_id) -> models.StreetAction | None:
        return await self.repository.get_street_action_by_id(street_action_id=action_id)

    @Game.get_current_player
    async def run(self, action_id: int) -> None:
        logger.debug(f"{self.user.email} Perform street action id {action_id}")
        action = await self.get_action(action_id=action_id)

        if not action:
            raise NotFoundException(f"Action is not found")
        if not self.player:
            raise PlayerException(f"Player is not found")

        self.set_player_harm( harm_action=action)
        self.update_balance(action=action)
        self.next_day()
        await self.session.commit()

    async def get_street_action_list(self) -> List[models.StreetAction]:
        return await self.repository.get_street_action_list()


class Work(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Work, self).__init__(session, user)
        self.repository = repository_entity.WorkEntity(session=session)

    async def get_action(self, work_id) -> models.Work | None:
        return await self.repository.get_work_by_id(work_id=work_id)

    @Game.get_current_player
    async def run(self, work_id: int) -> None:
        logger.debug(f"{self.user.email} Perform work id {work_id}")
        work = await self.get_action(work_id=work_id)

        if not work:
            raise NotFoundException(f"Work is not found")
        if not self.player:
            raise PlayerException(f"Player is not found")

        self.set_player_harm(harm_action=work)
        self.update_balance(action=work)
        self.next_day()
        await self.session.commit()

    async def get_work_list(self) -> List[models.Work]:
        return await self.repository.get_work_list()


class Food(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Food, self).__init__(session, user)
        self.repository = repository_entity.FoodEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_food_list(self) -> List[models.Food]:
        return await self.repository.get_food_list()


class Health(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Health, self).__init__(session, user)
        self.repository = repository_entity.HealthEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_health_list(self) -> List[models.Health]:
        return await self.repository.get_health_list()


class Leisure(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Leisure, self).__init__(session, user)
        self.repository = repository_entity.LeisureEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_leisure_list(self) -> List[models.Leisure]:
        return await self.repository.get_leisure_list()


class Business(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Business, self).__init__(session, user)
        self.repository = repository_entity.BusinessEntity(session=session)

    @Game.get_current_player
    def buy(self) -> None:
        ...

    async def get_business_list(self) -> List[models.Business]:
        return await self.repository.get_business_list()
