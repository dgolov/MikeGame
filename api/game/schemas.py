from datetime import datetime
from pydantic import BaseModel


class BenefitSchemaMixin:
    hunger_benefit_min: int
    hunger_benefit_max: int
    rest_benefit_min: int
    rest_benefit_max: int
    health_benefit_min: int
    health_benefit_max: int


class HarmSchemaMixin:
    hunger_harm_min: int
    hunger_harm_max: int
    rest_harm_min: int
    rest_harm_max: int
    health_harm_min: int
    health_harm_max: int


class PlayerBase(BaseModel):
    hunger: int
    rest: int
    health: int
    level: int
    age: int
    authority: int
    day: int

    class Config:
        from_attributes = True


class PlayerSchema(PlayerBase):
    user_id: int
    id: int


class CreatePlayer(PlayerBase):
    user_id: int


class UpdatePlayer(PlayerBase):
    pass


class CurrencyBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CurrencySchema(CurrencyBase):
    id: int


class CreateCurrency(CurrencyBase):
    pass


class UpdateCurrency(CurrencyBase):
    pass


class BalanceBase(BaseModel):
    name: str
    currency_id: int
    player_id: int
    amount: int

    class Config:
        from_attributes = True


class BalanceSchema(BalanceBase):
    id: int
    updated_at: datetime


class CreateBalance(BalanceBase):
    pass


class UpdateBalance(BalanceBase):
    pass


class HomeBase(BaseModel):
    name: str
    price: int

    class Config:
        from_attributes = True


class HomeSchema(HomeBase):
    id: int


class CreateHome(HomeBase):
    pass


class UpdateHome(HomeBase):
    pass


class SkillBase(BaseModel):
    name: str
    price: int

    class Config:
        from_attributes = True


class SkillSchema(SkillBase):
    id: int


class CreateSkill(SkillBase):
    pass


class UpdateSkill(SkillBase):
    pass


class TransportBase(BaseModel):
    name: str
    price: int
    skill_id: int

    class Config:
        from_attributes = True


class TransportSchema(TransportBase):
    id: int


class CreateTransport(TransportBase):
    pass


class UpdateTransport(TransportBase):
    pass


class StreetActionBase(BaseModel, HarmSchemaMixin):
    name: str
    income: int
    currency_id: int
    transport_id: int
    home_id: int
    skill_id: int

    class Config:
        from_attributes = True


class StreetActionSchema(StreetActionBase):
    id: int


class CreateStreetAction(StreetActionBase):
    pass


class UpdateStreetAction(StreetActionBase):
    pass


class WorkBase(BaseModel, HarmSchemaMixin):
    name: str
    income: int
    currency_id: int
    transport_id: int
    home_id: int
    skill_id: int

    class Config:
        from_attributes = True


class WorkSchema(WorkBase):
    id: int


class CreateWork(WorkBase):
    pass


class UpdateWork(WorkBase):
    pass


class FoodBase(BaseModel, BenefitSchemaMixin):
    name: str
    price: int

    class Config:
        from_attributes = True


class FoodSchema(FoodBase):
    id: int


class CreateFood(FoodBase):
    pass


class UpdateFood(FoodBase):
    pass


class HealthBase(BaseModel, BenefitSchemaMixin):
    name: str
    price: int

    class Config:
        from_attributes = True


class HealthSchema(HealthBase):
    id: int


class CreateHealth(HealthBase):
    pass


class UpdateHealth(HealthBase):
    pass


class LeisureBase(BaseModel, BenefitSchemaMixin):
    name: str
    price: int
    skill_id: int

    class Config:
        from_attributes = True


class LeisureSchema(LeisureBase):
    id: int


class CreateLeisure(LeisureBase):
    pass


class UpdateLeisure(LeisureBase):
    pass


class BusinessBase(BaseModel):
    name: str
    price: int
    income: int
    income_period: int
    currency_id: int
    transport_id: int
    home_id: int
    skill_id: int
    min_authority: int

    class Config:
        from_attributes = True


class BusinessSchema(BusinessBase):
    id: int


class CreateBusiness(BusinessBase):
    pass


class UpdateBusiness(BusinessBase):
    pass
