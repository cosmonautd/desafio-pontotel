"""create companies

Revision ID: 79cb0c2ded30
Revises: 
Create Date: 2020-10-14 13:49:22.470521

"""
import time

from alembic import op
import sqlalchemy as sa

from modules import alphavantage
from modules import config

# revision identifiers, used by Alembic.
revision = '79cb0c2ded30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

	companies_table = op.create_table(
		'companies',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('symbol', sa.String, nullable=False),
		sa.Column('name', sa.String),
        sa.Column('region', sa.String),
		sa.Column('marketOpen', sa.String),
		sa.Column('marketClose', sa.String),
		sa.Column('currency', sa.String)
	)

	# Fonte TOP 10 empresas brasileiras: https://www.meusdividendos.com/empresas/ranking
	# IBM será usada como exemplo para atualização em tempo real, visto que a função
	# intraday não está disponível para outras empresas.

	symbols = [
		'BRDT3.SAO', # Petrobras Distribuidora S.A.
		'ITUB3.SAO', # Itaú Unibanco Holding S.A.
		'VALE3.SAO', # Vale S.A.
		'OIBR3.SAO', # Oi S.A.
		'BBDC3.SAO', # Banco Bradesco S.A.
		'LIPR3.SAO', # Eletrobras Participações S.A. - Eletropar
		'BBAS3.SAO', # Banco do Brasi S.A.
		'SANB3.SAO', # Banco Santander (Brasil) S.A.
		'ABEV3.SAO', # Ambev S.A.
		'ITSA3.SAO'  # Itaúsa - Investimentos Itaú S.A.
	]

	companies = []
	alpha = alphavantage.AlphaMultiKeys(
		api_keys=config.get()['alphavantage_api_keys'],
		tor=True
	)

	# Essa operação demorar até 1 minuto
	# Pausas programadas são realizadas para respeitar os limites da API gratuita

	print('Iniciando população do BD...')

	for s in symbols:
		print('Adicionando %s...' % (s))
		result = alpha.search(keywords=s)
		company = result[0]
		companies.append({
			'symbol': s,
			'name': company['name'],
			'region': company['region'],
			'marketOpen': company['marketOpen'],
			'marketClose': company['marketClose'],
			'currency': company['currency'],
		})
		time.sleep(5)
	
	op.bulk_insert(
		companies_table,
		companies
	)


def downgrade():
	op.drop_table('companies')
