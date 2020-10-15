"""create users

Revision ID: f42421d945ed
Revises: 907494a11215
Create Date: 2020-10-14 19:27:42.426216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f42421d945ed'
down_revision = '907494a11215'
branch_labels = None
depends_on = None


def upgrade():
	companies_table = op.create_table(
		'users',
		sa.Column('id', sa.Integer, primary_key=True, index=True),
		sa.Column('username', sa.String(20), nullable=False),
		sa.Column('hashed_password', sa.String(64))
	)


def downgrade():
	op.drop_table('users')
