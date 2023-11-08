class Game:
    def __init__(self):
        ...

    def next_day(self):
        ...

    def _get_random_value(self, min_value, max_value):
        ...


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
