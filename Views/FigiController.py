
"""

 ---------------------------------------------------------------------------------------------------------------------------
|                                                                                                                          |
|                                                                                                                          |
|              This is the Controller for performing CRUD and Logic operations on openfigi relation relationship.                 |                                                                      |                                                    |
|                                                                                                                          |
 --------------------------------------------------------------------------------------------------------------------------|



"""

import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config,json 
from sqlalchemy import create_engine,asc,desc
from sqlalchemy.orm import sessionmaker,Session

from Providers.Alpaca import Alpaca
from datetime import date
from Helper.helpers import object_as_dict
from Model.app_db import Symbol,Figi




class Figi:


    def __init__(self):
        self.url=config.DB_URL
        self.Session=sessionmaker()




    def populate_figi_table(self):

        try:

            engine=create_engine(self.url)
            self.Session.configure(bind=engine)
            session=self.Session()


            symbols=session.query(Symbol.ticker).all()

            symbol_list=[{'idType': 'TICKER', 'idValue': symbol[0],} for symbol in symbols]


            







            # print(symbol_list)


            

        except Exception as e:
            raise e






obj=Figi()

obj.populate_figi_table()