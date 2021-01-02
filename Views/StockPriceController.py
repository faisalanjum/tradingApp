"""
|--------------------------------------------------------------------------------------------|
|                                                                                            |
|                                                                                            |
|        This is the Controller for performing CRUD and Logic operations on StockPrice       |
|         relationship.                                                                      |                                                    |
|                                                                                            |
|--------------------------------------------------------------------------------------------|

"""

import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from Model.app_db import StockPricesDaily





class StockPriceDailyController:
    

    def __init__(self):
        self.url=config.DB_URL
        self.Session=sessionmaker()




