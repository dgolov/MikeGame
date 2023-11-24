from core import repository_entity
from config import logger
from game import models, exceptions
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from users.models import User

import random


class Game:

    @staticmethod
    def get_current_player(func):
        def wrapper(self, *args, **kwargs):
            self.player = self.get_player()
            if not self.player:
                raise exceptions.PlayerException(f"Player is not found")
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    def __init__(self, session: AsyncSession, user: User):
        self.session = session
        self.user = user
        self.player = None
        self.repository = None

    def next_day(self) -> None:
        logger.debug(f"{self.user.email} Set next day")
        self.player.day += 1
        if 365 % self.player.day == 0:
            self.player.age += 1
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

        authority_benefit = self._get_authority_benefit(action=harm_action)

        if hunger_harm:
            self.player.hunger -= hunger_harm
        if rest_harm:
            self.player.rest -= rest_harm
        if health_harm:
            self.player.health -= health_harm
        if authority_benefit:
            self.player.authority += authority_benefit

        self.session.add(self.player)

    def set_player_benefit(
            self,
            benefit_action: models.Health | models.Food | models.Leisure
    ) -> None:
        """ Set benefit for player
        :param benefit_action: benefit action
        :return:
        """
        hunger_benefit = self._get_random_value(
            min_value=benefit_action.hunger_benefit_min,
            max_value=benefit_action.hunger_benefit_max
        )
        rest_benefit = self._get_random_value(
            min_value=benefit_action.rest_benefit_min,
            max_value=benefit_action.rest_benefit_max
        )
        health_benefit = self._get_random_value(
            min_value=benefit_action.health_benefit_min,
            max_value=benefit_action.health_benefit_max
        )

        authority_benefit = self._get_authority_benefit(action=benefit_action)

        if hunger_benefit:
            self.player.hunger += hunger_benefit
        if rest_benefit:
            self.player.rest += rest_benefit
        if health_benefit:
            self.player.health += health_benefit
        if authority_benefit:
            self.player.authority += authority_benefit

        self.session.add(self.player)

    def update_balance(
            self,
            action: Union[
                models.Food,
                models.Health,
                models.Transport,
                models.Home,
                models.Home,
                models.Skill,
                models.Work,
                models.Leisure,
                models.Business,
            ]
    ) -> None:
        """ Updated player balance after work or street action
        :param action: work or street action
        :param mode: increment or decrement
        :return:
        """
        mode = "increment"
        if hasattr(action, "price"):
            amount = -action.price
            mode = "decrement"
        else:
            amount = self._get_random_value(
                min_value=action.income_min,
                max_value=action.income_max
            )
        for balance in self.player.balances:
            if balance.currency.id == action.currency_id:
                if mode == "decrement":
                    self._check_balance(balance=balance, purchased_object=action)
                balance.amount += amount
                self.session.add(balance)

    def _check_balance(
            self,
            balance: models.Balance,
            purchased_object: Union[
                models.Food,
                models.Home,
                models.Skill,
                models.Leisure,
                models.Business,
                models.Transport,
                models.Health
            ]
    ) -> None:
        """ Check balance before purchasing
        :param balance:
        :param purchased_object:
        :return:
        """
        if balance.amount < purchased_object.price:
            logger.warning(
                f"{self.user.email} does not have enough money "
                f"to purchase {purchased_object} (id - {purchased_object.id})"
            )
            raise exceptions.NoMoneyError("You do not have enough money to make this purchase")

    def _check_object_in_player(
            self,
            object_model: Union[
                models.Transport, models.Home, models.Skill, models.Business
            ]
    ) -> None:
        """ Checks if the player has an object
        :param object_model:
        :return:
        """
        player_list_map = {
            "Transport": self.player.transport_list,
            "Home": self.player.home_list,
            "Skill": self.player.skills,
            "Business": self.player.business_list,
        }

        object_name = object_model.__class__.__name__
        player_list = player_list_map.get(object_name)
        if object_model in player_list:
            logger.warning(
                f"{self.user.email} {object_name} {object_model} (id - {object_model.id}) already exists"
            )
            raise exceptions.AlreadyExistError(f"{object_name} already exists")

    def _get_authority_benefit(self, action):
        """ Check authority_benefit fields and get random value
        :param action:
        :return:
        """
        authority_benefit = None
        if hasattr(action, "authority_benefit_min") and hasattr(action, "authority_benefit_max"):
            authority_benefit = self._get_random_value(
                min_value=action.authority_benefit_min,
                max_value=action.authority_benefit_max
            )
        return authority_benefit

    @staticmethod
    def _get_random_value(min_value: int, max_value: int) -> int:
        return random.randint(min_value, max_value)

    async def _get_by_id(
            self,
            object_id: int
    ) -> Union[
            models.Food,
            models.Health,
            models.Transport,
            models.Home,
            models.Home,
            models.Skill,
            models.Work,
            models.Leisure,
            models.Business,
            None
    ]:
        """ Get db object by id from repository
        :param object_id:
        :return:
        """
        return await self.repository.get_by_id(object_id=object_id)


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
    async def buy(self, home_id: int) -> None:
        logger.debug(f"{self.user.email} Buy home id {home_id}")
        home: models.Home | None = await self._get_by_id(object_id=home_id)

    async def get_home_list(self) -> List[models.Home]:
        return await self.repository.get_objects_list()


class Skill(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Skill, self).__init__(session, user)
        self.repository = repository_entity.SkillEntity(session=session)

    @Game.get_current_player
    async def buy(self, skill_id: int) -> None:
        logger.debug(f"{self.user.email} Buy skill id {skill_id}")
        skill: models.Skill | None = await self._get_by_id(object_id=skill_id)

    async def get_skill_list(self) -> List[models.Skill]:
        return await self.repository.get_skill_list()


class Transport(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Transport, self).__init__(session, user)
        self.repository = repository_entity.TransportEntity(session=session)

    @Game.get_current_player
    async def buy(self, transport_id: int) -> None:
        logger.debug(f"{self.user.email} Buy transport id {transport_id}")
        transport: models.Transport | None = await self._get_by_id(object_id=transport_id)

        if not transport:
            raise exceptions.NotFoundException(f"Transport {transport_id} is not found")

        self._check_object_in_player(object_model=transport)
        self.update_balance(action=transport)
        self.player.transport_list.append(transport)
        self.next_day()
        await self.session.commit()

    async def get_transport_list(self) -> List[models.Transport]:
        return await self.repository.get_objects_list()


class StreetAction(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(StreetAction, self).__init__(session, user)
        self.repository = repository_entity.StreetActionEntity(session=session)

    @Game.get_current_player
    async def run(self, action_id: int) -> None:
        logger.debug(f"{self.user.email} Perform street action id {action_id}")
        action: models.StreetAction | None = await self._get_by_id(object_id=action_id)

        if not action:
            raise exceptions.NotFoundException(f"Action {action_id} is not found")

        self.set_player_harm(harm_action=action)
        self.update_balance(action=action)
        self.next_day()
        await self.session.commit()

    async def get_street_action_list(self) -> List[models.StreetAction]:
        return await self.repository.get_objects_list()


class Work(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Work, self).__init__(session, user)
        self.repository = repository_entity.WorkEntity(session=session)

    @Game.get_current_player
    async def run(self, work_id: int) -> None:
        logger.debug(f"{self.user.email} Perform work id {work_id}")
        work: models.Work | None = await self._get_by_id(object_id=work_id)

        if not work:
            raise exceptions.NotFoundException(f"Work is not found")

        self.set_player_harm(harm_action=work)
        self.update_balance(action=work)
        self.next_day()
        await self.session.commit()

    async def get_work_list(self) -> List[models.Work]:
        return await self.repository.get_objects_list()


class Food(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Food, self).__init__(session, user)
        self.repository = repository_entity.FoodEntity(session=session)

    @Game.get_current_player
    async def buy(self, food_id: int) -> None:
        logger.debug(f"{self.user.email} Buy food id {food_id}")
        food: models.Food | None = await self._get_by_id(object_id=food_id)

        if not food:
            raise exceptions.NotFoundException(f"Food is not found")

        self.set_player_benefit(benefit_action=food)
        self.update_balance(action=food)
        self.next_day()
        await self.session.commit()

    async def get_food_list(self) -> List[models.Food]:
        return await self.repository.get_objects_list()


class Health(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Health, self).__init__(session, user)
        self.repository = repository_entity.HealthEntity(session=session)

    @Game.get_current_player
    async def buy(self, health_id: int) -> None:
        logger.debug(f"{self.user.email} Buy health id {health_id}")
        health: models.Health | None = await self._get_by_id(object_id=health_id)

        if not health:
            raise exceptions.NotFoundException(f"Health is not found")

        self.set_player_benefit(benefit_action=health)
        self.update_balance(action=health)
        self.next_day()
        await self.session.commit()

    async def get_health_list(self) -> List[models.Health]:
        return await self.repository.get_objects_list()


class Leisure(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Leisure, self).__init__(session, user)
        self.repository = repository_entity.LeisureEntity(session=session)

    @Game.get_current_player
    async def buy(self, leisure_id) -> None:
        logger.debug(f"{self.user.email} Buy leisure id {leisure_id}")
        leisure: models.Leisure | None = await self._get_by_id(object_id=leisure_id)

        if not leisure:
            raise exceptions.NotFoundException(f"Leisure is not found")

        self.set_player_benefit(benefit_action=leisure)
        self.update_balance(action=leisure)
        self.next_day()
        await self.session.commit()

    async def get_leisure_list(self) -> List[models.Leisure]:
        return await self.repository.get_objects_list()


class Business(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Business, self).__init__(session, user)
        self.repository = repository_entity.BusinessEntity(session=session)

    @Game.get_current_player
    async def buy(self, business_id) -> None:
        logger.debug(f"{self.user.email} Buy business id {business_id}")
        business: models.Business | None = await self._get_by_id(object_id=business_id)

    async def get_business_list(self) -> List[models.Business]:
        return await self.repository.get_objects_list()
