"""create quotes

Revision ID: 907494a11215
Revises: 79cb0c2ded30
Create Date: 2020-10-14 19:17:03.844696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '907494a11215'
down_revision = '79cb0c2ded30'
branch_labels = None
depends_on = None


def upgrade():
	# Definição da tabela de cotações
	quotes_table = op.create_table(
		'quotes',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('open', sa.Float),
		sa.Column('high', sa.Float),
		sa.Column('low', sa.Float),
		sa.Column('price', sa.Float),
		sa.Column('volume', sa.Integer),
		sa.Column('latest_trading_day', sa.String),
		sa.Column('previous_close', sa.Float),
		sa.Column('change', sa.Float),
		sa.Column('change_percent', sa.Float),
		sa.Column('created_at', sa.DateTime(timezone=True)),
		sa.Column('equity_symbol', sa.String, sa.ForeignKey('equities.symbol'), index=True)
	)


def downgrade():
	op.drop_table('quotes')
