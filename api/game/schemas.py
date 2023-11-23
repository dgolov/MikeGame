from datetime import datetime
from typing import List
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
    amount: int

    class Config:
        from_attributes = True


class BalanceSchema(BalanceBase):
    id: int
    updated_at: datetime
    currency: CurrencySchema


class CreateBalance(BalanceBase):
    currency_id: int
    player_id: int


class UpdateBalance(BalanceBase):
    currency_id: int
    player_id: int


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
    balances: List[BalanceSchema]


class CreatePlayer(PlayerBase):
    user_id: int


class UpdatePlayer(PlayerBase):
    pass


class HomeBase(BaseModel):
    name: str
    description: str | None
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
    description: str | None

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
    description: str | None
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


class ActionBaseSchema:
    name: str
    description: str | None
    income_min: int
    income_max: int
    currency_id: int
    transport_id: int | None
    home_id: int | None
    skill_id: int | None


class StreetActionBase(BaseModel, ActionBaseSchema, HarmSchemaMixin):
    authority_benefit_min: int | None
    authority_benefit_max: int | None

    class Config:
        from_attributes = True


class StreetActionSchema(StreetActionBase):
    id: int


class CreateStreetAction(StreetActionBase):
    pass


class UpdateStreetAction(StreetActionBase):
    pass


class PerformActionSchema(BaseModel):
    id: int


class WorkBase(BaseModel, ActionBaseSchema, HarmSchemaMixin):
    pass

    class Config:
        from_attributes = True


class WorkSchema(WorkBase):
    id: int


class CreateWork(WorkBase):
    pass


class UpdateWork(WorkBase):
    pass


class PerformWorkSchema(BaseModel):
    id: int


class FoodBase(BaseModel, BenefitSchemaMixin):
    name: str
    description: str | None
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
    description: str | None
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
    description: str | None
    price: int
    skill_id: int
    authority_benefit_min: int | None
    authority_benefit_max: int | None

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
    description: str | None
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
