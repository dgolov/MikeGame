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
        self.object_model = None

    def next_day(self) -> None:
        """ Set next day
        :return:
        """
        logger.debug(f"{self.user.email} Set next day")
        self.player.day += 1
        if 365 % self.player.day == 0:
            self.player.age += 1
        self._check_dead()
        self.session.add(self.player)

    def get_player(self) -> models.Player | None:
        """ Get item player by current user
        :return:
        """
        try:
            return self.user.players[-1]
        except IndexError:
            logger.error(f"Player is not exist for user - {self.user.email}")

    async def buy_item(self) -> None:
        """ Buy item (Transport, Home, Business, Skill)
        :return:
        """
        if not self.object_model:
            raise exceptions.NotFoundException(
                f"{self.object_model.__class__.__name__} {self.object_model} is not found"
            )
        self._check_object_in_player()
        self.update_balance()
        self.player.transport_list.append(self.object_model)
        self.next_day()
        await self.session.commit()

    async def buy_service(self) -> None:
        """ Buy service (Health, Food, Leisure)
        :return:
        """
        if not self.object_model:
            raise exceptions.NotFoundException(
                f"{self.object_model.__class__.__name__} is not found"
            )
        self.set_player_benefit()
        self.update_balance()
        self.next_day()
        await self.session.commit()

    async def perform_action(self) -> None:
        """ Perform action (Work, Street action)
        :return:
        """
        if not self.object_model:
            raise exceptions.NotFoundException(
                f"{self.object_model.__class__.__name__} is not found"
            )

        self.check_availability()
        self.set_player_harm()
        self.update_balance()
        self.next_day()

        await self.session.commit()

    def set_player_harm(self) -> None:
        """ Set harm for player
        :return:
        """
        hunger_harm: int = self._get_random_value(
            min_value=self.object_model.hunger_harm_min,
            max_value=self.object_model.hunger_harm_max
        )
        rest_harm: int = self._get_random_value(
            min_value=self.object_model.rest_harm_min,
            max_value=self.object_model.rest_harm_max
        )
        health_harm: int = self._get_random_value(
            min_value=self.object_model.health_harm_min,
            max_value=self.object_model.health_harm_max
        )

        authority_benefit: int = self._get_authority_benefit()

        if hunger_harm:
            self.player.hunger -= hunger_harm
        if rest_harm:
            self.player.rest -= rest_harm
        if health_harm:
            self.player.health -= health_harm
        if authority_benefit:
            self.player.authority += authority_benefit

        self.session.add(self.player)

    def set_player_benefit(self) -> None:
        """ Set benefit for player
        :return:
        """
        hunger_benefit: int = self._get_random_value(
            min_value=self.object_model.hunger_benefit_min,
            max_value=self.object_model.hunger_benefit_max
        )
        rest_benefit: int = self._get_random_value(
            min_value=self.object_model.rest_benefit_min,
            max_value=self.object_model.rest_benefit_max
        )
        health_benefit: int = self._get_random_value(
            min_value=self.object_model.health_benefit_min,
            max_value=self.object_model.health_benefit_max
        )

        authority_benefit: int = self._get_authority_benefit()

        if hunger_benefit:
            self.player.hunger += hunger_benefit
        if rest_benefit:
            self.player.rest += rest_benefit
        if health_benefit:
            self.player.health += health_benefit
        if authority_benefit:
            self.player.authority += authority_benefit

        self.session.add(self.player)

    def update_balance(self) -> None:
        """ Updated player balance after work or street action
        :return:
        """
        mode = "increment"
        if hasattr(self.object_model, "price") and self.object_model.price:
            amount = -self.object_model.price
            mode = "decrement"
        else:
            amount: int = self._get_random_value(
                min_value=self.object_model.income_min,
                max_value=self.object_model.income_max
            )
        for balance in self.player.balances:
            if balance.currency.id == self.object_model.currency_id:
                if mode == "decrement":
                    self._check_balance(balance=balance, purchased_object=self.object_model)
                balance.amount += amount
                self.session.add(balance)

    def check_availability(self) -> None:
        """ Checking the player's transport, home or skill availability
        :return:
        """
        possibility_list = ("transport", "home", "skill")

        for possibility in possibility_list:
            if not self._check_availability(possibility_str=possibility):
                raise exceptions.NoPossibilityError(
                    f"You do not have suitable {possibility} - {getattr(self.object_model, possibility)}"
                )

    def _check_availability(self, possibility_str: str) -> bool:
        """ Checking item availability
        :param possibility_str:
        :return:
        """
        if not hasattr(self.object_model, possibility_str):
            return True

        possibility = getattr(self.object_model, possibility_str)

        if hasattr(self.player, f"{possibility_str}_list"):
            player_possibility_list = getattr(self.player, f"{possibility_str}_list")
        else:
            player_possibility_list = getattr(self.player, f"{possibility_str}s")

        if possibility and possibility in player_possibility_list:
            return True
        elif not possibility:
            return True

        return False

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

    def _check_object_in_player(self) -> None:
        """ Checks if the player has an object
        :return:
        """
        player_list_map = {
            "Transport": self.player.transport_list,
            "Home": self.player.home_list,
            "Skill": self.player.skills,
            "Business": self.player.business_list,
        }

        object_name = self.object_model.__class__.__name__
        player_list = player_list_map.get(object_name, None)
        if self.object_model in player_list:
            logger.warning(
                f"{self.user.email} {object_name} {self.object_model} already exists"
            )
            raise exceptions.AlreadyExistError(f"{object_name} already exists")

    def _get_authority_benefit(self) -> int | None:
        """ Check authority_benefit fields and get random value
        :return:
        """
        authority_benefit = None
        if hasattr(self.object_model, "authority_benefit_min") \
                and hasattr(self.object_model, "authority_benefit_max"):
            if not self.object_model.authority_benefit_min or not self.object_model.authority_benefit_max:
                return
            authority_benefit = self._get_random_value(
                min_value=self.object_model.authority_benefit_min,
                max_value=self.object_model.authority_benefit_max
            )
        return authority_benefit

    @staticmethod
    def _get_random_value(min_value: int, max_value: int) -> int:
        """ Random(min, max)
        :param min_value:
        :param max_value:
        :return:
        """
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

    def _check_dead(self) -> None:
        """ Check if player is dead
        :return:
        """
        dead_mode = False

        for attr in ("hunger", "rest", "health"):
            if getattr(self.player, attr) <= 0:
                setattr(self.player, attr, 0)
                dead_mode = True
            elif getattr(self.player, attr) >= 100:
                setattr(self.player, attr, 100)

        if dead_mode:
            self.player.deadly_days += 1
        else:
            if self.player.deadly_days:
                self.player.deadly_days = 0

        if self.player.deadly_days > 7:
            self.player.alive = False


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
        """ Add new player for user
        :return:
        """
        self.default_player_data["user_id"] = self.user.id
        player_id = await self.repository.create(
            data=self.default_player_data
        )
        logger.info(
            f"[Logic.Player] Add new player (id - {player_id}) by user id - {self.user.id}"
        )

    async def get_info(self) -> models.Player | None:
        """ Get player info
        :return:
        """
        return self.get_player()


class Home(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Home, self).__init__(session, user)
        self.repository = repository_entity.HomeEntity(session=session)

    @Game.get_current_player
    async def buy(self, home_id: int) -> None:
        """ Buy home
        :param home_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy home id {home_id}")
        self.object_model: models.Home | None = await self._get_by_id(object_id=home_id)
        await self.buy_item()

    async def get_home_list(self) -> List[models.Home]:
        """ Home list
        :return:
        """
        return await self.repository.get_objects_list()


class Skill(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Skill, self).__init__(session, user)
        self.repository = repository_entity.SkillEntity(session=session)

    @Game.get_current_player
    async def buy(self, skill_id: int) -> None:
        """ Buy skill
        :param skill_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy skill id {skill_id}")
        self.object_model: models.Skill | None = await self._get_by_id(object_id=skill_id)
        await self.buy_item()

    async def get_skill_list(self) -> List[models.Skill]:
        """ Skill list
        :return:
        """
        return await self.repository.get_objects_list()


class Transport(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Transport, self).__init__(session, user)
        self.repository = repository_entity.TransportEntity(session=session)

    @Game.get_current_player
    async def buy(self, transport_id: int) -> None:
        """ Buy transport
        :param transport_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy transport id {transport_id}")
        self.object_model: models.Transport | None = await self._get_by_id(object_id=transport_id)
        await self.buy_item()

    async def get_transport_list(self) -> List[models.Transport]:
        """ Transport list
        :return:
        """
        return await self.repository.get_objects_list()


class StreetAction(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(StreetAction, self).__init__(session, user)
        self.repository = repository_entity.StreetActionEntity(session=session)

    @Game.get_current_player
    async def run(self, action_id: int) -> None:
        """ Perform street action
        :param action_id:
        :return:
        """
        logger.debug(f"{self.user.email} Perform street action id {action_id}")
        self.object_model: models.StreetAction | None = await self._get_by_id(object_id=action_id)
        await self.perform_action()

    async def get_street_action_list(self) -> List[models.StreetAction]:
        """ StreetAction list
        :return:
        """
        return await self.repository.get_objects_list()


class Work(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Work, self).__init__(session, user)
        self.repository = repository_entity.WorkEntity(session=session)

    @Game.get_current_player
    async def run(self, work_id: int) -> None:
        """ Perform work action
        :param work_id:
        :return:
        """
        logger.debug(f"{self.user.email} Perform work id {work_id}")
        self.object_model: models.Work | None = await self._get_by_id(object_id=work_id)
        await self.perform_action()

    async def get_work_list(self) -> List[models.Work]:
        """ Work list
        :return:
        """
        return await self.repository.get_objects_list()


class Food(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Food, self).__init__(session, user)
        self.repository = repository_entity.FoodEntity(session=session)

    @Game.get_current_player
    async def buy(self, food_id: int) -> None:
        """ Buy food
        :param food_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy food id {food_id}")
        self.object_model: models.Food | None = await self._get_by_id(object_id=food_id)

        await self.buy_service()

    async def get_food_list(self) -> List[models.Food]:
        """ Food list
        :return:
        """
        return await self.repository.get_objects_list()


class Health(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Health, self).__init__(session, user)
        self.repository = repository_entity.HealthEntity(session=session)

    @Game.get_current_player
    async def buy(self, health_id: int) -> None:
        """ Buy health
        :param health_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy health id {health_id}")
        self.object_model: models.Health | None = await self._get_by_id(object_id=health_id)
        await self.buy_service()

    async def get_health_list(self) -> List[models.Health]:
        """ Health list
        :return:
        """
        return await self.repository.get_objects_list()


class Leisure(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Leisure, self).__init__(session, user)
        self.repository = repository_entity.LeisureEntity(session=session)

    @Game.get_current_player
    async def buy(self, leisure_id) -> None:
        """ Buy leisure
        :param leisure_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy leisure id {leisure_id}")
        self.object_model: models.Leisure | None = await self._get_by_id(object_id=leisure_id)
        await self.buy_service()

    async def get_leisure_list(self) -> List[models.Leisure]:
        """ Leisure list
        :return:
        """
        return await self.repository.get_objects_list()


class Business(Game):
    def __init__(self, session: AsyncSession, user: User):
        super(Business, self).__init__(session, user)
        self.repository = repository_entity.BusinessEntity(session=session)

    @Game.get_current_player
    async def buy(self, business_id) -> None:
        """ Buy business
        :param business_id:
        :return:
        """
        logger.debug(f"{self.user.email} Buy business id {business_id}")
        self.object_model: models.Business | None = await self._get_by_id(object_id=business_id)
        self.check_availability()
        if self.object_model.min_authority > self.player.authority:
            raise exceptions.NoPossibilityError(f"You do not have suitable authority")
        await self.buy_item()

    async def get_business_list(self) -> List[models.Business]:
        """ Business list
        :return:
        """
        return await self.repository.get_objects_list()
