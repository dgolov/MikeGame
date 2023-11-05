"""init

Revision ID: 3402d1642cd6
Revises: 
Create Date: 2023-11-05 00:38:00.622602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3402d1642cd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currency_id'), 'currency', ['id'], unique=True)
    op.create_index(op.f('ix_currency_name'), 'currency', ['name'], unique=False)
    op.create_table('food',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('hunger_benefit_min', sa.Integer(), nullable=True),
    sa.Column('hunger_benefit_max', sa.Integer(), nullable=True),
    sa.Column('rest_benefit_min', sa.Integer(), nullable=True),
    sa.Column('rest_benefit_max', sa.Integer(), nullable=True),
    sa.Column('health_benefit_min', sa.Integer(), nullable=True),
    sa.Column('health_benefit_max', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_id'), 'food', ['id'], unique=True)
    op.create_index(op.f('ix_food_name'), 'food', ['name'], unique=False)
    op.create_table('health',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('hunger_benefit_min', sa.Integer(), nullable=True),
    sa.Column('hunger_benefit_max', sa.Integer(), nullable=True),
    sa.Column('rest_benefit_min', sa.Integer(), nullable=True),
    sa.Column('rest_benefit_max', sa.Integer(), nullable=True),
    sa.Column('health_benefit_min', sa.Integer(), nullable=True),
    sa.Column('health_benefit_max', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_health_id'), 'health', ['id'], unique=True)
    op.create_index(op.f('ix_health_name'), 'health', ['name'], unique=False)
    op.create_table('home',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_id'), 'home', ['id'], unique=True)
    op.create_index(op.f('ix_home_name'), 'home', ['name'], unique=False)
    op.create_table('player',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hunger', sa.Integer(), nullable=False),
    sa.Column('rest', sa.Integer(), nullable=False),
    sa.Column('health', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('authority', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_id'), 'player', ['id'], unique=True)
    op.create_table('skill',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skill_id'), 'skill', ['id'], unique=True)
    op.create_index(op.f('ix_skill_name'), 'skill', ['name'], unique=False)
    op.create_table('balance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_balance_id'), 'balance', ['id'], unique=True)
    op.create_index(op.f('ix_balance_name'), 'balance', ['name'], unique=False)
    op.create_table('leisure',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.Column('hunger_benefit_min', sa.Integer(), nullable=True),
    sa.Column('hunger_benefit_max', sa.Integer(), nullable=True),
    sa.Column('rest_benefit_min', sa.Integer(), nullable=True),
    sa.Column('rest_benefit_max', sa.Integer(), nullable=True),
    sa.Column('health_benefit_min', sa.Integer(), nullable=True),
    sa.Column('health_benefit_max', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leisure_id'), 'leisure', ['id'], unique=True)
    op.create_index(op.f('ix_leisure_name'), 'leisure', ['name'], unique=False)
    op.create_table('transport',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transport_id'), 'transport', ['id'], unique=True)
    op.create_index(op.f('ix_transport_name'), 'transport', ['name'], unique=False)
    op.create_table('business',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('income', sa.Integer(), nullable=False),
    sa.Column('income_period', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('transport_id', sa.Integer(), nullable=True),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.Column('min_authority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.ForeignKeyConstraint(['transport_id'], ['transport.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_business_id'), 'business', ['id'], unique=True)
    op.create_index(op.f('ix_business_name'), 'business', ['name'], unique=False)
    op.create_table('street_action',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('income', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('transport_id', sa.Integer(), nullable=True),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.Column('hunger_harm_min', sa.Integer(), nullable=True),
    sa.Column('hunger_harm_max', sa.Integer(), nullable=True),
    sa.Column('rest_harm_min', sa.Integer(), nullable=True),
    sa.Column('rest_harm_max', sa.Integer(), nullable=True),
    sa.Column('health_harm_min', sa.Integer(), nullable=True),
    sa.Column('health_harm_max', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.ForeignKeyConstraint(['transport_id'], ['transport.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_street_action_id'), 'street_action', ['id'], unique=True)
    op.create_index(op.f('ix_street_action_name'), 'street_action', ['name'], unique=False)
    op.create_table('work',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('income', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('transport_id', sa.Integer(), nullable=True),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.Column('hunger_harm_min', sa.Integer(), nullable=True),
    sa.Column('hunger_harm_max', sa.Integer(), nullable=True),
    sa.Column('rest_harm_min', sa.Integer(), nullable=True),
    sa.Column('rest_harm_max', sa.Integer(), nullable=True),
    sa.Column('health_harm_min', sa.Integer(), nullable=True),
    sa.Column('health_harm_max', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.ForeignKeyConstraint(['transport_id'], ['transport.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_id'), 'work', ['id'], unique=True)
    op.create_index(op.f('ix_work_name'), 'work', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_work_name'), table_name='work')
    op.drop_index(op.f('ix_work_id'), table_name='work')
    op.drop_table('work')
    op.drop_index(op.f('ix_street_action_name'), table_name='street_action')
    op.drop_index(op.f('ix_street_action_id'), table_name='street_action')
    op.drop_table('street_action')
    op.drop_index(op.f('ix_business_name'), table_name='business')
    op.drop_index(op.f('ix_business_id'), table_name='business')
    op.drop_table('business')
    op.drop_index(op.f('ix_transport_name'), table_name='transport')
    op.drop_index(op.f('ix_transport_id'), table_name='transport')
    op.drop_table('transport')
    op.drop_index(op.f('ix_leisure_name'), table_name='leisure')
    op.drop_index(op.f('ix_leisure_id'), table_name='leisure')
    op.drop_table('leisure')
    op.drop_index(op.f('ix_balance_name'), table_name='balance')
    op.drop_index(op.f('ix_balance_id'), table_name='balance')
    op.drop_table('balance')
    op.drop_index(op.f('ix_skill_name'), table_name='skill')
    op.drop_index(op.f('ix_skill_id'), table_name='skill')
    op.drop_table('skill')
    op.drop_index(op.f('ix_player_id'), table_name='player')
    op.drop_table('player')
    op.drop_index(op.f('ix_home_name'), table_name='home')
    op.drop_index(op.f('ix_home_id'), table_name='home')
    op.drop_table('home')
    op.drop_index(op.f('ix_health_name'), table_name='health')
    op.drop_index(op.f('ix_health_id'), table_name='health')
    op.drop_table('health')
    op.drop_index(op.f('ix_food_name'), table_name='food')
    op.drop_index(op.f('ix_food_id'), table_name='food')
    op.drop_table('food')
    op.drop_index(op.f('ix_currency_name'), table_name='currency')
    op.drop_index(op.f('ix_currency_id'), table_name='currency')
    op.drop_table('currency')
    # ### end Alembic commands ###