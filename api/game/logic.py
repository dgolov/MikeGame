from core import repository_entity
from config import logger
from game import models
from users.models import User


class Game:
    def __init__(self, session, user: User):
        self.session = session
        self.user = user

    def next_day(self):
        ...

    def _get_random_value(self, min_value, max_value):
        ...


class Player(Game):
    def __init__(self, session, user: User):
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
        super(Game, self).__init__(session, user)

    async def add_player(self):
        self.default_player_data["user_id"] = self.user.id
        player_id = await repository_entity.PlayerEntity(session=self.session).create(
            data=self.default_player_data
        )
        logger.info(
            f"[Logic.Player] Add new player (id - {player_id}) by user id - {self.user.id}"
        )


class Home(Game):
    def __init__(self, session, user: User):
        super(Home, self).__init__(session, user)

    def buy(self):
        ...


class Skill(Game):
    def __init__(self, session, user: User):
        super(Skill, self).__init__(session, user)

    def buy(self):
        ...


class Transport(Game):
    def __init__(self, session, user: User):
        super(Transport, self).__init__(session, user)

    def buy(self):
        ...


class StreetAction(Game):
    def __init__(self, session, user: User):
        super(StreetAction, self).__init__(session, user)

    def run(self):
        ...


class Work(Game):
    def __init__(self, session, user: User):
        super(Work, self).__init__(session, user)

    def run(self):
        ...


class Food(Game):
    def __init__(self, session, user: User):
        super(Food, self).__init__(session, user)

    def buy(self):
        ...


class Health(Game):
    def __init__(self, session, user: User):
        super(Health, self).__init__(session, user)

    def buy(self):
        ...


class Leisure(Game):
    def __init__(self, session, user: User):
        super(Leisure, self).__init__(session, user)

    def buy(self):
        ...


class Business(Game):
    def __init__(self, session, user: User):
        super(Business, self).__init__(session, user)

    def buy(self):
        ...
