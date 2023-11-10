from core import repository_entity
from core.engine import get_async_session
from config import logger


class Game:
    def __init__(self):
        ...

    def next_day(self):
        ...

    def _get_random_value(self, min_value, max_value):
        ...


class Player(Game):
    def __init__(self):
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
        super(Game, self).__init__()

    async def add_player(self, user_id: int, session):
        logger.info(
            f"[Logic.Player] Add new player by user id - {user_id}"
        )
        self.default_player_data["user_id"] = user_id
        await repository_entity.PlayerEntity(session=session).create(
            data=self.default_player_data
        )


class Home(Game):
    def __init__(self):
        super(Home, self).__init__()

    def buy(self):
        ...


class Skill(Game):
    def __init__(self):
        super(Skill, self).__init__()

    def buy(self):
        ...


class Transport(Game):
    def __init__(self):
        super(Transport, self).__init__()

    def buy(self):
        ...


class StreetAction(Game):
    def __init__(self):
        super(StreetAction, self).__init__()

    def run(self):
        ...


class Work(Game):
    def __init__(self):
        super(Work, self).__init__()

    def run(self):
        ...


class Food(Game):
    def __init__(self):
        super(Food, self).__init__()

    def buy(self):
        ...


class Health(Game):
    def __init__(self):
        super(Health, self).__init__()

    def buy(self):
        ...


class Leisure(Game):
    def __init__(self):
        super(Leisure, self).__init__()

    def buy(self):
        ...


class Business(Game):
    def __init__(self):
        super(Business, self).__init__()

    def buy(self):
        ...
