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
	# Definição da tabela de usuários
	companies_table = op.create_table(
		'users',
		sa.Column('username', sa.String, primary_key=True, index=True),
		sa.Column('hashed_password', sa.String)
	)


def downgrade():
	op.drop_table('users')
