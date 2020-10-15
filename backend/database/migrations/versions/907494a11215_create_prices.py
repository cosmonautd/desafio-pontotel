"""create prices

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
	prices_table = op.create_table(
		'prices',
		sa.Column('id', sa.Integer, primary_key=True, index=True),
		sa.Column('open', sa.Float),
		sa.Column('close', sa.Float),
		sa.Column('high', sa.Float),
		sa.Column('low', sa.Float),
		sa.Column('volume', sa.Integer),
		sa.Column('period', sa.Enum("intraday", "daily", "weekly", 'monthly', name='period_enum')),
		sa.Column('time', sa.String),
		sa.Column('company_id', sa.Integer, sa.ForeignKey('companies.id'))
	)


def downgrade():
	op.drop_table('prices')
