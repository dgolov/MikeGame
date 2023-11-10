from core.engine import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship


home_player = Table(
    "home_player", Base.metadata,
    Column("home_id", ForeignKey("home.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("player_id", ForeignKey("player.id", ondelete="CASCADE"), primary_key=True)
)


skill_player = Table(
    "skill_player", Base.metadata,
    Column("skill_id", ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("player_id", ForeignKey("player.id", ondelete="CASCADE"), primary_key=True)
)


transport_player = Table(
    "transport_player", Base.metadata,
    Column("transport_id", ForeignKey("transport.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("player_id", ForeignKey("player.id", ondelete="CASCADE"), primary_key=True)
)


business_player = Table(
    "business_player", Base.metadata,
    Column("business_id", ForeignKey("business.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("player_id", ForeignKey("player.id", ondelete="CASCADE"), primary_key=True)
)


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    hunger = Column(Integer, nullable=False)
    rest = Column(Integer, nullable=False)
    health = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    authority = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    home_list = relationship(
        "Home",
        secondary=home_player,
        lazy="selectin",
        join_depth=2
    )
    skills = relationship(
        "Skill",
        secondary=skill_player,
        lazy="selectin",
        join_depth=2
    )
    transport_list = relationship(
        "Transport",
        secondary=transport_player,
        lazy="selectin",
        join_depth=2
    )
    business_list = relationship(
        "Business",
        secondary=business_player,
        lazy="selectin",
        join_depth=2
    )


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)


class Balance(Base):
    __tablename__ = "balance"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    currency = relationship("Currency", lazy="selectin")
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    player = relationship("Player", lazy="selectin")
    amount = Column(Integer, nullable=False)
    updated_at = Column(DateTime)


class Home(Base):
    __tablename__ = "home"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)


class Skill(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)


class Transport(Base):
    __tablename__ = "transport"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.id'))
    skill = relationship("Skill", lazy="selectin")


class StreetAction(Base):
    __tablename__ = "street_action"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    income = Column(Integer, nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    currency = relationship("Currency", lazy="selectin")
    transport_id = Column(Integer, ForeignKey('transport.id'))
    transport = relationship("Transport", lazy="selectin")
    home_id = Column(Integer, ForeignKey('home.id'))
    home = relationship("Home", lazy="selectin")
    skill_id = Column(Integer, ForeignKey('skill.id'))
    skill = relationship("Skill", lazy="selectin")
    hunger_harm_min = Column(Integer)
    hunger_harm_max = Column(Integer)
    rest_harm_min = Column(Integer)
    rest_harm_max = Column(Integer)
    health_harm_min = Column(Integer)
    health_harm_max = Column(Integer)


class Work(Base):
    __tablename__ = "work"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    income = Column(Integer, nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    currency = relationship("Currency", lazy="selectin")
    transport_id = Column(Integer, ForeignKey('transport.id'))
    transport = relationship("Transport", lazy="selectin")
    home_id = Column(Integer, ForeignKey('home.id'))
    home = relationship("Home", lazy="selectin")
    skill_id = Column(Integer, ForeignKey('skill.id'))
    skill = relationship("Skill", lazy="selectin")
    hunger_harm_min = Column(Integer)
    hunger_harm_max = Column(Integer)
    rest_harm_min = Column(Integer)
    rest_harm_max = Column(Integer)
    health_harm_min = Column(Integer)
    health_harm_max = Column(Integer)


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    hunger_benefit_min = Column(Integer)
    hunger_benefit_max = Column(Integer)
    rest_benefit_min = Column(Integer)
    rest_benefit_max = Column(Integer)
    health_benefit_min = Column(Integer)
    health_benefit_max = Column(Integer)


class Health(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    hunger_benefit_min = Column(Integer)
    hunger_benefit_max = Column(Integer)
    rest_benefit_min = Column(Integer)
    rest_benefit_max = Column(Integer)
    health_benefit_min = Column(Integer)
    health_benefit_max = Column(Integer)


class Leisure(Base):
    __tablename__ = "leisure"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.id'))
    skill = relationship("Skill", lazy="selectin")
    hunger_benefit_min = Column(Integer)
    hunger_benefit_max = Column(Integer)
    rest_benefit_min = Column(Integer)
    rest_benefit_max = Column(Integer)
    health_benefit_min = Column(Integer)
    health_benefit_max = Column(Integer)


class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    income = Column(Integer, nullable=False)
    income_period = Column(Integer, nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    currency = relationship("Currency", lazy="selectin")
    transport_id = Column(Integer, ForeignKey('transport.id'))
    transport = relationship("Transport", lazy="selectin")
    home_id = Column(Integer, ForeignKey('home.id'))
    home = relationship("Home", lazy="selectin")
    skill_id = Column(Integer, ForeignKey('skill.id'))
    skill = relationship("Skill", lazy="selectin")
    min_authority = Column(Integer)
