import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy import ForeignKey,Date,BigInteger,Float,Text,DateTime,String,Time
from sqlalchemy.sql import func
from sqlalchemy import Enum, UniqueConstraint
import enum
from sqlalchemy.event import listens_for



Base = declarative_base()

# Vendor Table
 
class Vendor(Base):
   
   #tablename

    __tablename__="vendors"

   #column_schema 
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    vendor_id=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())
   


# Exchange Table

class Exchange(Base):
    __tablename__ = "exchange"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    acronmy=Column(String)
    mic=Column(String)
    timezone_offset=Column(DateTime,nullable=False)
    country=Column(String,nullable=False)
    currency=Column(String,nullable=False)



#Symbol Table

class Symbol(Base):
    __tablename__="symbol"
    id=Column(Integer,primary_key=True,autoincrement=True)
    provided_by=Column(Integer,ForeignKey("vendors.id"))
    exchange_id=Column(Integer,ForeignKey("exchange.id"))
    currency=Column(String,nullable=False)
    ticker=Column(String,nullable=False)
    instrument=Column(String,nullable=False)
    name=Column(String,nullable=False)
    figi=Column(String,nullable=True)
    composite_figi=Column(String,nullable=True)
    share_class_figi=Column(String,nullable=True)
    share_class=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())   
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    exchange=relationship("Exchange",backref="symbol_exchange")
    vendor=relationship("Vendor",backref="symbol_vendors")
    

#Company Table


class Company(Base):
    __tablename__="company"
    id=Column(Integer,primary_key=True)
    symbol_id=Column(Integer,ForeignKey("symbol.id"))
    name=Column(Text,nullable=False)
    cik=Column(String,nullable=False)
    sector=Column(String,nullable=False)
    industry_category=Column(String,nullable=False)
    industry_group=Column(String,nullable=False)
    company_url=Column(String,nullable=False)
    description=Column(Text,nullable=True)
    sic=Column(String)
    symbol=relationship('Symbol',backref="company_symbol")





#stockPrices Daily

class StockPricesDaily(Base):
    __tablename__="stock_prices_daily"
    id=Column(Integer,primary_key=True)
    company_id=Column(Integer,ForeignKey('company.id'))
    vendor_id=Column(Integer,ForeignKey('vendors.id'))
    datetime=Column(DateTime,nullable=False)
    open=Column(Float,nullable=False)
    high=Column(Float,nullable=False)
    low=Column(Float,nullable=False)
    close=Column(Float,nullable=False)
    volume=Column(BigInteger,nullable=False) 
    adj_open=Column(Float,nullable=False)
    adj_high=Column(Float,nullable=False)
    adj_low=Column(Float,nullable=False)
    adj_close=Column(Float,nullable=False)
    adj_volume=Column(Float,nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True) , onupdate=func.now())
    company=relationship("Company",backref='company_details')
    vendor=relationship("Vendor",backref="vendor_details")


#stockPrices Daily

class StockPricesIntraday(Base):
    __tablename__="stock_prices_intraday"
    id=Column(Integer,primary_key=True)
    company_id=Column(Integer,ForeignKey('company.id'))
    vendor_id=Column(Integer,ForeignKey('vendors.id'))
    datetime=Column(DateTime,nullable=False)
    open=Column(Float,nullable=False)
    high=Column(Float,nullable=False)
    low=Column(Float,nullable=False)
    close=Column(Float,nullable=False)
    volume=Column(BigInteger,nullable=False) 
    adj_open=Column(Float,nullable=False)
    adj_high=Column(Float,nullable=False)
    adj_low=Column(Float,nullable=False)
    adj_close=Column(Float,nullable=False)
    adj_volume=Column(Float,nullable=False)
    frequency=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    company_details=relationship("Company",backref='company_info')
    vendor=relationship("Vendor",backref="vendor_info")

#StockAdjustments

class StockAdjustment(Base):
   


    __tablename__="stock_adjustment"
    
    id=Column(Integer,primary_key=True)
    vendor=Column(Integer,ForeignKey('vendors.id'))
    company=Column(Integer,ForeignKey('company.id'))
    datetime=Column(DateTime,nullable=False)
    divident_amount=Column(Float, nullable=False)
    split_coef=Column(Float,nullable=False)
    shares_outstanding=Column(BigInteger,nullable=False)








class FinancialStatementType(enum.Enum):
    balance_sheet = 'balance sheet'
    income_statement = 'income statement'
    cash_flow_statement = 'cash flow statement'


class FinancialStatementPeriod(enum.Enum):
    fy = 'fy'
    q1 = 'q1'
    q2 = 'q2'
    q3 = 'q3'
    q4 = 'q4'


class FinancialStatement(Base):
    __tablename__ = 'financial_statement'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)


class FinancialStatementLine(Base):
    __tablename__ = 'financial_statement_line'
    id = Column(Integer, primary_key=True)
    tag = Column(String(50), nullable=False, unique=True)
    name = Column('name', String(100), nullable=False, unique=True)
    description = Column('description', String(1000))
    sequences = relationship('FinancialStatementLineSequence', backref='line')
    facts = relationship('FinancialStatementFact', backref='line')


class FinancialStatementLineSequence(Base):
    __tablename__ = 'financial_statement_line_sequence'
    id = Column(Integer, primary_key=True)
    sequence = Column('sequence', Integer, nullable=False)
    financial_statement_id = Column(Integer,
                                    ForeignKey('financial_statement.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    nullable=False)
    financial_statement_line_id = Column(Integer,
                                         ForeignKey('financial_statement_line.id',
                                                    onupdate='CASCADE',
                                                    ondelete='CASCADE'),
                                         nullable=False)
    UniqueConstraint('financial_statement_id',
                     'financial_statement_line_id')
    financial_statement = relationship('FinancialStatement')
    financial_statement_line = relationship('FinancialStatementLine')


class FinancialStatementLineAlias(Base):
    __tablename__ = 'financial_statement_line_alias'
    id = Column(Integer, primary_key=True)
    alias = Column(String(200), nullable=False, unique=True)
    financial_statement_line_id = Column(Integer,
                                         ForeignKey('financial_statement_line.id',
                                                    onupdate='CASCADE',
                                                    ondelete='CASCADE'),
                                         nullable=False)
    financial_statement_line = relationship('FinancialStatementLine')


class FinancialStatementFact(Base):
    __tablename__ = 'financial_statement_fact'
    __table_args__ = tuple(
        [UniqueConstraint('company_id',
                          'financial_statement_line_id',
                          'fiscal_year',
                          'fiscal_period')])
    id = Column(Integer, primary_key=True)
    vendor_id=Column(Integer,ForeignKey("vendors.id"),nullable=False)
    fiscal_year = Column('fiscal_year', Integer, nullable=False)
    fiscal_period = Column('fiscal_period',
                           Enum(FinancialStatementPeriod),
                           nullable=False)
    filing_date = Column('filing_date', Date, nullable=False)
    start_date = Column('start_date', Date)
    end_date = Column('end_date', Date, nullable=False)
    amount = Column('amount', Float, nullable=False)
    company_id = Column(Integer,
                        ForeignKey('company.id',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'),
                        nullable=False)
    financial_statement_line_id = Column(
                                    Integer,
                                    ForeignKey('financial_statement_line.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    nullable=False)

    company = relationship("Company")

commercial_income_statement = FinancialStatement(name='Commercial Income Statement')
commercial_balance_sheet = FinancialStatement(name='Commercial Balance Sheet Statement')
commercial_cash_flow_statement = FinancialStatement(name='Commercial Cash Flow Statement')

financial_income_statement = FinancialStatement(name='Financial Income Statement')
financial_balance_sheet = FinancialStatement(name='Financial Balance Sheet Statement')
financial_cash_flow_statement = FinancialStatement(name='Financial Cash Flow Statement')


@listens_for(FinancialStatement.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    session.add(commercial_income_statement)
    session.add(commercial_balance_sheet)
    session.add(commercial_cash_flow_statement)
    session.add(financial_income_statement)
    session.add(financial_balance_sheet)
    session.add(financial_cash_flow_statement)
    session.commit()

@listens_for(FinancialStatementLine.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    financial_statement_lines = pd.read_csv('financial_statements_lines.csv')
    financial_statement_lines = financial_statement_lines[['tag', 'name']].drop_duplicates('tag')

    for index, line in financial_statement_lines.iterrows():
        session.add(FinancialStatementLine(tag=line['tag'], name=line['name']))
    session.commit()        

@listens_for(FinancialStatementLineSequence.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    financial_statement_lines = pd.read_csv('financial_statements_lines.csv')
    statement_types = ['commercial', 'financial']
    statement_codes = ['income_statement', 'balance_sheet_statement', 'cash_flow_statement']
    
    for statement_type in statement_types:
        for statement_code in statement_codes:
            statement_name = (statement_type + ' ' + statement_code.replace('_',' ')).title()
            statement = session.query(FinancialStatement) \
                .filter(FinancialStatement.name == statement_name).one()
            financial_statement_sequence = financial_statement_lines[
                (financial_statement_lines['statement_type'] == statement_type) & \
                (financial_statement_lines['statement_code'] == statement_code)]
            
            for index, row in financial_statement_sequence.iterrows():
                line = session.query(FinancialStatementLine) \
                    .filter(FinancialStatementLine.tag == row['tag']).one()
                session.add(FinancialStatementLineSequence(sequence=row['sequence'],
                                                        financial_statement_id=statement.id,
                                                        financial_statement_line_id=line.id))
    session.commit()



class User(Base):

    #tablename

    __tablename__="users"


    #columns
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    alpaca_id=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now())


#strategy_table

class Strategy(Base):

    #tablename
    __tablename__="strategy"
    
    #columns
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    create_by=Column(Integer,ForeignKey("users.id"))
    description=Column(Text,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now())
    
    #relationship
    user=relationship('User',back_populates="user_details")
    



#Strategyexecuted table 

class StrategyExecuted(Base):
    
    #tablename
    __tablename__="strategies_executed"

    
    #columns
    id=Column(Integer,primary_key=True)
    executed_by=Column(Integer,ForeignKey("users.id"))
    strategy_executed=Column(Integer,ForeignKey("strategy.id"))
    executed_on=Column(Integer,ForeignKey("symbol.id"))
    order_placed=Column(Boolean,default=0)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now())
    
    #relationships
    user=relationship("User",back_populates="users_info")
    strategy=relationship("Strategy",back_populates="strategy_info")
    security=relationship("Symbol",back_populates="security_info")







#orders table

class Orders(Base):

    #tablename
    __tablename__="orders"


    #columns
    
    id=Column(Integer,primary_key=True)
    ordered_by=Column(Integer,ForeignKey("users.id"))
    through_strategy=Column(Integer,ForeignKey("strategies_executed.id"))
    order_date=Column(DateTime(timezone=True),server_default=func.now())
    order_updated=Column(DateTime(timezone=True),server_default=func.now())

    #relationships
    desc=relationship("StrategyExecuted",backref="Strategy_details")





