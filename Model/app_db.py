import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy import ForeignKey,Date,BigInteger,Float,Text,DateTime,String,Time,Sequence
from sqlalchemy.sql import func
from sqlalchemy import Enum, UniqueConstraint,PrimaryKeyConstraint
import enum 
from sqlalchemy.event import listens_for



Base = declarative_base()




class User(Base):

    #tablename

    __tablename__="users"

    

    #columns
    id=Column("id",Integer,primary_key=True)


    name=Column("name",String,nullable=False)
    alpaca_secret=Column("alpaca_secret",String,nullable=False)
    alpaca_key=Column("alpaca_key",String,nullable=False)
    created_at=Column("created_at",DateTime(timezone=True),server_default=func.now())
    updated_at=Column("updated_at",DateTime(timezone=True),server_default=func.now())

    







# Vendor Table
 
class Vendor(Base):
   
   #tablename

    __tablename__="vendors"
    __table_args__=tuple([UniqueConstraint("name")])

   #column_schema 
    id=Column("id",Integer,primary_key=True)
    name=Column("name",String,nullable=False)
    vendor_id=Column("vendor_id",String,nullable=True)
    created_at=Column("created_at",DateTime(timezone=True), server_default=func.now())
    updated_at=Column("updated_at",DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Vendor(id='%s',name='%s', vendor_id='%s', created_at='%s',updated_at='%s')>" % (
                             self.id,self.name, self.vendor_id, self.created_at,self.updated_at)
   


# Exchange Table

class Exchange(Base):
    __tablename__ = "exchange"
    id=Column(Integer,autoincrement=True)
    exchange_id=Column(String,primary_key=True)
    mic=Column(String)
    name=Column(String,nullable=False)
    acronmy=Column(String)
    
    timezone_offset=Column(DateTime)
    country=Column(String)
    currency=Column(String)
    



#Symbol Table

class Symbol(Base):
    __tablename__="symbol"
    __table_args__ = tuple([UniqueConstraint('ticker')])
    id=Column(Integer,Sequence("symbol_id_seq"),primary_key=True,autoincrement=True)
    provided_by=Column(Integer,ForeignKey("vendors.id"))
    exchange_Acr=Column(String)
    ticker=Column(String)
    name=Column(String,nullable=False)

    # relationship

    
    
    figi_details=relationship("Figi")

    prices_interday=relationship("StockPricesIntraday",backref="symbol")

    prices_daily=relationship("StockPricesDaily",backref="symbol")




class Figi(Base):

    __tablename__="openfigi"
    id=Column(Integer,primary_key=True,autoincrement=True)
    figi=Column(String)
    name=Column(String)
    ticker=Column(String,ForeignKey("symbol.ticker"))
    exchCode=Column(String)
    compositeFigi=Column(String)
    uniqueID=Column(String)
    securityType=Column(String)
    marketSector=Column(String)
    shareClassFigi=Column(String)
    uniqueIDFutOpt=Column(String)
    securityType2=Column(String)
    securityDescription=Column(String)

    

#Company Table


class Company(Base):
    __tablename__="company"
    id=Column(Integer,primary_key=True)
    symbol_id=Column(String,ForeignKey("symbol.ticker"))
    name=Column(Text,nullable=False)
    cik=Column(String,nullable=False)
    sector=Column(String,nullable=False)
    industry_category=Column(String,nullable=False)
    industry_group=Column(String,nullable=False)
    company_url=Column(String,nullable=False)
    description=Column(Text,nullable=True)
    sic=Column(String)
    symbol=relationship('Symbol')
    
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True) , onupdate=func.now())






    

#stockPrices Daily

class StockPricesIntraday(Base):
    __tablename__="stock_prices_intraday"
    id=Column(Integer,primary_key=True)

    __table_args__=tuple([UniqueConstraint('vendor_id', 'stock_symbol', "datetime")])
    
    vendor_id=Column(Integer,ForeignKey('vendors.id'))
    stock_symbol=Column(String,ForeignKey("symbol.ticker"),nullable=False)
    datetime=Column(DateTime,nullable=False)
    open=Column(Float,nullable=False)
    high=Column(Float,nullable=False)
    low=Column(Float,nullable=False)
    close=Column(Float,nullable=False)
    volume=Column(BigInteger,nullable=False) 
    adj_open=Column(Float,nullable=True)
    adj_high=Column(Float,nullable=True)
    adj_low=Column(Float,nullable=True)
    adj_close=Column(Float,nullable=True)
    adj_volume=Column(Float,nullable=True)
    frequency=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    








#stockPrices Daily

class StockPricesDaily(Base):
    __tablename__="stock_prices_daily"
    id=Column(Integer,primary_key=True)
    __table_args__=tuple([UniqueConstraint('vendor_id', 'stock_symbol', "datetime")])
    vendor_id=Column(Integer,ForeignKey('vendors.id'),nullable=True)
    stock_symbol=Column(String,ForeignKey("symbol.ticker"))
    datetime=Column(DateTime,nullable=False)
    open=Column(Float,nullable=False)
    high=Column(Float,nullable=False)
    low=Column(Float,nullable=False)
    close=Column(Float,nullable=False)
    volume=Column(BigInteger,nullable=False) 
    adj_open=Column(Float,nullable=True)
    adj_high=Column(Float,nullable=True)
    adj_low=Column(Float,nullable=True)
    adj_close=Column(Float,nullable=True)
    adj_volume=Column(Float,nullable=True)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True) , onupdate=func.now())
   
    
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




class Strategy(Base):

    #tablename
    __tablename__="strategy"
    
    #columns
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    created_by=Column(Integer,ForeignKey("users.id"))
    description=Column(Text,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now())
    
    #relationship
   



#Strategyexecuted table 

class StrategyExecuted(Base):
    
    #tablename
    __tablename__="strategies_executed"

    
    #columns
    id=Column(Integer,primary_key=True)
    executed_by=Column(Integer,ForeignKey("users.id"))
    strategy_executed=Column(Integer,ForeignKey("strategy.id"))
    executed_on=Column(String,ForeignKey("symbol.ticker"))
    order_placed=Column(Boolean,default=0)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now())
    
    #relationships
    
   




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
    desc=relationship("StrategyExecuted",backref="strategy")





#relationship














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





#strategy_table

