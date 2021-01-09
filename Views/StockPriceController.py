

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
from Model.app_db import StockPricesDaily,Vendor,Symbol,StockPricesIntraday
from Providers.Alpaca import Alpaca
from datetime import date
from Helper.helpers import object_as_dict
import pandas as pd



class StockPriceController:
    def __init__(self):
        self.url=config.DB_URL
        self.Session=sessionmaker()
    


    def hist_stock_pri_pvd(self,provider_name,frequncy,stock_symbol=None,historical=True,start=None,end=None,price_type="daily"):



        '''
        Fetches the list of stocks_prices from the provider (ALPACA) or anyother.generates a list of dic for the Symbol Mapper
        & adds records to the table 
        


        Parameters
         ----------
        provider_name : str()
            provider name.



        stock_symbol:str( )
            "day" or "1D" for day
            "1Min" for one minute data
            "5Min" for five finute data
            "15Min" for fifteen min data






       start:datetime string in format yyyy-mm-dd



       end:datatime str() in yyyy-mm-dd format


       price_type:str()

       "daily" to get daily data 
       "inter" 
            


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
            if historical == True and price_type=="daily":

                start=pd.Timestamp('2008-01-01', tz='America/New_York').isoformat()
                end=pd.Timestamp('today', tz='America/New_York').isoformat()





            elif historical==False and price_type=="daily":

                start=pd.Timestamp('today', tz='America/New_York').isoformat()



            elif historical==True and price_type=="intraday":
                start=pd.Timestamp('2015-01-01', tz='America/New_York').isoformat()
                end=pd.Timestamp('today', tz='America/New_York').isoformat()


            else:

                start=pd.Timestamp('today', tz='America/New_York').isoformat()


















            api=Alpaca()

            if stock_symbol == None:
                barsets=api.getStockPrices(timeframe=frequncy,start=start,end=end)

            elif type(stock_symbol) == list :

                barsets=api.getStockPrices(stock_symbol,timeframe=frequncy,start=start,end=end)


           
             

            keylist=[] 

            stockPrices=[]


            for item in barsets:
                keys, values = list(item.items())[0]
                keylist.append(keys)

            


            

            for i in range(len(keylist)):

                

                barset=barsets[i][keylist[i]]

                
                for bar in barset:



                    if price_type=="daily":
                        dct={"vendor_id":int(vendor_id),
                            "stock_symbol":str(keylist[i]),
                            "datetime": bar.t.date(),
                            "open":bar.o,
                            "high":bar.h,
                            "low":bar.l,
                            "close":bar.c,
                            "volume":bar.v,}

                    else:
                        dct={"vendor_id":int(vendor_id),
                            "stock_symbol":str(keylist[i]),
                            "datetime": bar.t,
                            "open":bar.o,
                            "high":bar.h,
                            "low":bar.l,
                            "close":bar.c,
                            "volume":bar.v,
                            "frequency":frequncy,}




                    

                    stockPrices.append(dct)


            
            #bulk inserts into the Symbol table
            
            if price_type=="daily":
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
            elif price_type=="intraday":

                try:
                    session=self.Session()
                    session.bulk_insert_mappings(StockPricesIntraday,stockPrices)
                except Exception as e:
                    raise e
                    print(f"There was some Error inserting data Error:{e}")
                    session.rollback()
                finally:
                    print("records added to the table")

                    session.commit()


            else:



                print("select a right argument for price_type choices are daily,intraday")
    




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

            

            stockPrices=session.query(StockPricesDaily).filter(StockPricesDaily.stock_symbol.in_(stockList) ).order_by(StockPricesDaily.datetime.desc()).all()

            

            


             
            
                
        else:
            stockPrices=session.query(StockPricesDaily).order_by(StockPricesDaily.stock_symbol.desc(),StockPricesDaily.datetime.desc()).all()

       
                
        return stockPrices




















            