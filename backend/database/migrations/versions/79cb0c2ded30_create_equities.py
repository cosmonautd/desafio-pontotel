"""create equities

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

	# Definição da tabela de patrimônios
	equities_table = op.create_table(
		'equities',
		sa.Column('symbol', sa.String, primary_key=True, index=True),
		sa.Column('name', sa.String),
        sa.Column('region', sa.String),
		sa.Column('market_open', sa.String),
		sa.Column('market_close', sa.String),
		sa.Column('currency', sa.String),
		sa.Column('type', sa.String)
	)

	# Fonte TOP 10 empresas brasileiras: https://www.meusdividendos.com/empresas/ranking
	symbols = [
		[config.get('bovespa'), 'index'],
		['BRDT3.SAO', 'company'], # Petrobras Distribuidora S.A.
		['ITUB3.SAO', 'company'], # Itaú Unibanco Holding S.A.
		['VALE3.SAO', 'company'], # Vale S.A.
		['OIBR3.SAO', 'company'], # Oi S.A.
		['BBDC3.SAO', 'company'], # Banco Bradesco S.A.
		['LIPR3.SAO', 'company'], # Eletrobras Participações S.A. - Eletropar
		['BBAS3.SAO', 'company'], # Banco do Brasi S.A.
		['SANB3.SAO', 'company'], # Banco Santander (Brasil) S.A.
		['ABEV3.SAO', 'company'], # Ambev S.A.
		['ITSA3.SAO', 'company']  # Itaúsa - Investimentos Itaú S.A.
	]

	# Cria objeto AlphaMultiKeys para interação com Alpha Vantage
	equities = []
	alpha = alphavantage.AlphaMultiKeys(
		api_keys=config.get('alphavantage_api_keys'),
		tor=True
	)

	# Essa operação demorar até 1 minuto
	# Pausas programadas são realizadas para respeitar alguns limites da API gratuita

	print('Iniciando população do BD...')

	for s, type_ in symbols:
		print('Buscando %s...' % (s))
		result = alpha.search(keywords=s)
		equity = result[0]
		equities.append({
			'symbol': s,
			'name': equity['name'],
			'region': equity['region'],
			'market_open': equity['market_open'],
			'market_close': equity['market_close'],
			'currency': equity['currency'],
			'type': type_
		})
		time.sleep(5)
	
	# Insere os patrimônios encontrados no banco de dados
	op.bulk_insert(
		equities_table,
		equities
	)


def downgrade():
	op.drop_table('equities')
