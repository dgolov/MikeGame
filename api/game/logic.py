from core import repository_entity
from config import logger
from game import models
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from users.models import User


class Game:
    def __init__(self, session: AsyncSession, user: User):
        self.session = session
        self.user = user

    def next_day(self) -> None:
        ...

    def _get_random_value(self, min_value: int, max_value: int) -> int:
        ...


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
        try:
            player = self.user.players[-1]
        except IndexError:
            logger.error(f"Player is not exist for user - {self.user.email}")
            return

        return await self.repository.get_player_by_id(
            player_id=player.id
        )


class Home(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Home, self).__init__(session, user)
        self.repository = repository_entity.HomeEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_home_list(self) -> List[models.Home]:
        return await self.repository.get_home_list()


class Skill(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Skill, self).__init__(session, user)
        self.repository = repository_entity.SkillEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_skill_list(self) -> List[models.Skill]:
        return await self.repository.get_skill_list()


class Transport(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Transport, self).__init__(session, user)
        self.repository = repository_entity.TransportEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_transport_list(self) -> List[models.Transport]:
        return await self.repository.get_transport_list()


class StreetAction(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(StreetAction, self).__init__(session, user)
        self.repository = repository_entity.StreetActionEntity(session=session)

    def run(self) -> None:
        ...

    async def get_street_action_list(self) -> List[models.StreetAction]:
        return await self.repository.get_street_action_list()


class Work(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Work, self).__init__(session, user)
        self.repository = repository_entity.WorkEntity(session=session)

    def run(self) -> None:
        ...

    async def get_work_list(self) -> List[models.Work]:
        return await self.repository.get_work_list()


class Food(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Food, self).__init__(session, user)
        self.repository = repository_entity.FoodEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_food_list(self) -> List[models.Food]:
        return await self.repository.get_food_list()


class Health(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Health, self).__init__(session, user)
        self.repository = repository_entity.HealthEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_health_list(self) -> List[models.Health]:
        return await self.repository.get_health_list()


class Leisure(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Leisure, self).__init__(session, user)
        self.repository = repository_entity.LeisureEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_leisure_list(self) -> List[models.Leisure]:
        return await self.repository.get_leisure_list()


class Business(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Business, self).__init__(session, user)
        self.repository = repository_entity.BusinessEntity(session=session)

    def buy(self) -> None:
        ...

    async def get_business_list(self) -> List[models.Business]:
        return await self.repository.get_business_list()
