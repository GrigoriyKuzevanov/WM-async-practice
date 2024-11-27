"""create spimexresult model

Revision ID: 48e69b77576f
Revises: 
Create Date: 2024-11-22 11:29:54.696952+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48e69b77576f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('spimex_trading_results',
    sa.Column('exchange_product_id', sa.String(), nullable=False),
    sa.Column('exchange_product_name', sa.String(), nullable=False),
    sa.Column('oil_id', sa.String(), nullable=False),
    sa.Column('delivery_basis_id', sa.String(), nullable=False),
    sa.Column('delivery_basis_name', sa.String(), nullable=False),
    sa.Column('delivery_type_id', sa.String(), nullable=False),
    sa.Column('volume', sa.Integer(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_spimex_trading_results'))
    )


def downgrade() -> None:
    op.drop_table('spimex_trading_results')
