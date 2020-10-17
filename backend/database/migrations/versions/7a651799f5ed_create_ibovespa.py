"""create ibovespa

Revision ID: 7a651799f5ed
Revises: f42421d945ed
Create Date: 2020-10-17 11:23:54.682953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a651799f5ed'
down_revision = 'f42421d945ed'
branch_labels = None
depends_on = None


def upgrade():
	ibovespa_table = op.create_table(
		'ibovespa',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('open', sa.Float),
		sa.Column('high', sa.Float),
		sa.Column('low', sa.Float),
		sa.Column('price', sa.Float),
		sa.Column('volume', sa.Integer),
		sa.Column('latest_trading_day', sa.String),
		sa.Column('previous_close', sa.Float),
		sa.Column('change', sa.Float),
		sa.Column('change_percent', sa.Float)
	)


def downgrade():
	op.drop_table('ibovespa')

