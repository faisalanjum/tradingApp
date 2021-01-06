

"""

 ---------------------------------------------------------------------------------------------------------------------------
|                                                                                                                          |
|                                                                                                                          |
|              This is the Controller for performing CRUD and Logic operations on StockPrice relationship.                 |                                                                      |                                                    |
|                                                                                                                          |
 --------------------------------------------------------------------------------------------------------------------------|



"""

import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config,json 
from sqlalchemy import create_engine,asc,desc
from sqlalchemy.orm import sessionmaker,Session
from Model.app_db import StockPricesDaily,Vendor
from Providers.Alpaca import Alpaca
from datetime import date
from Helper.helpers import object_as_dict



class StockPriceDailyController:
    def __init__(self):
        self.url=config.DB_URL
        self.Session=sessionmaker()
    


    def hist_stock_pri_pvd(self,provider_name,stock_symbol=None):



        '''
        Fetches the list of stocks_prices from the provider (ALPACA) or anyother.generates a list of dic for the Symbol Mapper
        & adds records to the table 
        


        Parameters
         ----------
        provider_name : str()
            provider name.



        stock_list:list( )
            A list of stock symbols that conform to the Alpaca API request structure.


        list of stocks


  
        Returns
        -------
        
        Nothing

            
        '''

        #engine created


        engine=create_engine(self.url)
        self.Session.configure(bind=engine)
        session=self.Session()

        # checks for vendor
        try:
            vendor_id = session.query(Vendor.id).filter(Vendor.name == provider_name).one()[0]
        except Exception as  e:
            print("no record found for provider")
        







        #records from alpaca
        
        if provider_name=="Alpaca":
            api=Alpaca()

            if stock_symbol == None:
                barsets=api.getStockPrices()

            elif type(stock_symbol) == list :

                barsets=api.getStockPrices(stock_symbol)



             

            keylist=[] 

            stockPrices=[]


            for item in barsets:
                keys, values = list(item.items())[0]
                keylist.append(keys)

            


            

            for i in range(len(keylist)):

                

                barset=barsets[i][keylist[i]]

                
                for bar in barset:

                   
                    dct={"vendor_id":int(vendor_id),
                        "stock_symbol":str(keylist[i]),
                        "datetime": bar.t.date(),
                        "open":bar.o,
                        "high":bar.h,
                        "low":bar.l,
                        "close":bar.c,
                        "volume":bar.v,}



                    

                    stockPrices.append(dct)



            #bulk inserts into the Symbol table
            

            try:
                session=self.Session()
                session.bulk_insert_mappings(StockPricesDaily,stockPrices)
            except Exception as e:
                raise e
                print(f"There was some Error inserting data Error:{e}")
                session.rollback()
            finally:
                print("records added to the table")

                session.commit()
        

    def getDailyPrices(self,symbol=None,frm_date=None,to_date=None,adjusted=False):
        '''
            Get's the record from the table based on the symbol ,timeframe 
        


            Parameters
            ----------
            symbol : (str),(list),or (none) for all stocks
            A list of stock symbols that are in the database.

            frm_date:date iso string 

            to_date:date is string


            adjusted:(Bool) (default=False without adjusted prices) ,set (True) to get adjusted price 

  
            Returns
            -------
        
            json list of prices

            
        '''

        engine=create_engine(self.url)
        self.Session.configure(bind=engine)

        session=self.Session()

        
        if symbol !=  None :

            stockList=[]


            if type(symbol) == str:
                stockList.append(symbol)
            else:
                stockList=symbol

            

            stockPrices=session.query(StockPricesDaily).filter(StockPricesDaily.stock_symbol.in_(stockList) ).all()

            

            


             
            
                
        else:
            stockPrices=session.query(StockPricesDaily).order_by(StockPricesDaily.stock_symbol.desc(),StockPricesDaily.datetime.desc()).all()

       
                
        return [object_as_dict(price) for price in stockPrices]





















            

        




obj=StockPriceDailyController()


obj.hist_stock_pri_pvd("Alpaca",stock_symbol=["MSFT"])

# prices=obj.getDailyPrices(symbol=["ACIA","AAPL"])

# print(prices)

# print(prices)


