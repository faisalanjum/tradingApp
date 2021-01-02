"""empty message

Revision ID: 2776c9693592
Revises: 
Create Date: 2021-01-01 16:26:08.388756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2776c9693592'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('acronmy', sa.String(), nullable=True),
    sa.Column('mic', sa.String(), nullable=True),
    sa.Column('timezone_offset', sa.DateTime(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('financial_statement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('financial_statement_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('tag')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('alpaca_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vendors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('vendor_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('financial_statement_line_alias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alias', sa.String(length=200), nullable=False),
    sa.Column('financial_statement_line_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['financial_statement_line_id'], ['financial_statement_line.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('alias')
    )
    op.create_table('financial_statement_line_sequence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sequence', sa.Integer(), nullable=False),
    sa.Column('financial_statement_id', sa.Integer(), nullable=False),
    sa.Column('financial_statement_line_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['financial_statement_id'], ['financial_statement.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['financial_statement_line_id'], ['financial_statement_line.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strategy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('create_by', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['create_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('symbol',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('provided_by', sa.Integer(), nullable=True),
    sa.Column('exchange_id', sa.Integer(), nullable=True),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=False),
    sa.Column('instrument', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('figi', sa.String(), nullable=True),
    sa.Column('composite_figi', sa.String(), nullable=True),
    sa.Column('share_class_figi', sa.String(), nullable=True),
    sa.Column('share_class', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['exchange_id'], ['exchange.id'], ),
    sa.ForeignKeyConstraint(['provided_by'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('cik', sa.String(), nullable=False),
    sa.Column('sector', sa.String(), nullable=False),
    sa.Column('industry_category', sa.String(), nullable=False),
    sa.Column('industry_group', sa.String(), nullable=False),
    sa.Column('company_url', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('sic', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbol.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strategies_executed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('executed_by', sa.Integer(), nullable=True),
    sa.Column('strategy_executed', sa.Integer(), nullable=True),
    sa.Column('executed_on', sa.Integer(), nullable=True),
    sa.Column('order_placed', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['executed_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['executed_on'], ['symbol.id'], ),
    sa.ForeignKeyConstraint(['strategy_executed'], ['strategy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('financial_statement_fact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('fiscal_year', sa.Integer(), nullable=False),
    sa.Column('fiscal_period', sa.Enum('fy', 'q1', 'q2', 'q3', 'q4', name='financialstatementperiod'), nullable=False),
    sa.Column('filing_date', sa.Date(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('financial_statement_line_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['financial_statement_line_id'], ['financial_statement_line.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company_id', 'financial_statement_line_id', 'fiscal_year', 'fiscal_period')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ordered_by', sa.Integer(), nullable=True),
    sa.Column('through_strategy', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('order_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['ordered_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['through_strategy'], ['strategies_executed.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_adjustment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vendor', sa.Integer(), nullable=True),
    sa.Column('company', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('divident_amount', sa.Float(), nullable=False),
    sa.Column('split_coef', sa.Float(), nullable=False),
    sa.Column('shares_outstanding', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['company'], ['company.id'], ),
    sa.ForeignKeyConstraint(['vendor'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_prices_daily',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('open', sa.Float(), nullable=False),
    sa.Column('high', sa.Float(), nullable=False),
    sa.Column('low', sa.Float(), nullable=False),
    sa.Column('close', sa.Float(), nullable=False),
    sa.Column('volume', sa.BigInteger(), nullable=False),
    sa.Column('adj_open', sa.Float(), nullable=False),
    sa.Column('adj_high', sa.Float(), nullable=False),
    sa.Column('adj_low', sa.Float(), nullable=False),
    sa.Column('adj_close', sa.Float(), nullable=False),
    sa.Column('adj_volume', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_prices_intraday',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('open', sa.Float(), nullable=False),
    sa.Column('high', sa.Float(), nullable=False),
    sa.Column('low', sa.Float(), nullable=False),
    sa.Column('close', sa.Float(), nullable=False),
    sa.Column('volume', sa.BigInteger(), nullable=False),
    sa.Column('adj_open', sa.Float(), nullable=False),
    sa.Column('adj_high', sa.Float(), nullable=False),
    sa.Column('adj_low', sa.Float(), nullable=False),
    sa.Column('adj_close', sa.Float(), nullable=False),
    sa.Column('adj_volume', sa.Float(), nullable=False),
    sa.Column('frequency', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_prices_intraday')
    op.drop_table('stock_prices_daily')
    op.drop_table('stock_adjustment')
    op.drop_table('orders')
    op.drop_table('financial_statement_fact')
    op.drop_table('strategies_executed')
    op.drop_table('company')
    op.drop_table('symbol')
    op.drop_table('strategy')
    op.drop_table('financial_statement_line_sequence')
    op.drop_table('financial_statement_line_alias')
    op.drop_table('vendors')
    op.drop_table('users')
    op.drop_table('financial_statement_line')
    op.drop_table('financial_statement')
    op.drop_table('exchange')
    # ### end Alembic commands ###