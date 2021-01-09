

"""
|--------------------------------------------------------------------------------------------|
|                                                                                            |
|                                                                                            |
|        THIS CLASS iMPLEMENTS THE CRUD OPERATION AND BUSINESS LOGIC ON THE VENDOR TABLE     | 
|                                                                                            |
|                                                                                            |
|--------------------------------------------------------------------------------------------|
"""

import sys,os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config
from Helper.helpers import divide_chunks,remove_dupe_dicts,object_as_dict
from Providers.Alpaca import Alpaca
from Providers.OpenFigi import OpenFigi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from Model.app_db import Symbol,Vendor
import time,json







class SymbolController:
    



    def __init__(self):
        self.url=config.DB_URL
        self.Session=sessionmaker()
        #creates database session
        engine=create_engine(self.url)
        self.Session.configure(bind=engine)

        





    def bulkInsertFromProviders(self,provider_name):
        '''
        Fetches the list of stocks from the provider (ALPACA).generates a list of dic for the Symbol Mapper
        & adds records to the table 
        


        Parameters
         ----------
        provider_name : str()
            A list of stock symbols that conform to the Alpaca API request structure.
  
        Returns
        -------
        
        Nothing

            
        '''

       
        session=self.Session()
        

        #fetch from the vendor table vendor associated with name 


        try:
            vendor_id = session.query(Vendor.id).filter(Vendor.name == provider_name).one()[0]
                
        except Exception as  e:
            print("no record found for provider")

        


        #establish connection with the alpaca through Alpaca module 

        alpaca=Alpaca()
        asset_list=alpaca.getAssetList()
        

        #creates a list of Dict for Symbol table

        alpaca_dict=[{ "provided_by":int(vendor_id),"exchange_Acr":getattr(asset,"exchange"),"ticker":getattr(asset,"symbol"),"name":getattr(asset,"name")} for asset in asset_list]
        
        unique_dict=remove_dupe_dicts(alpaca_dict)
        


        
        #bulk inserts into the Symbol table


        try:
            session=self.Session()
            session.bulk_insert_mappings(Symbol,unique_dict)
        except Exception as e:
            raise e
            print(f"There was some Error inserting data Error:{e}")
            session.rollback()
        finally:
            print("records added to the table")

            session.commit()
          

   


    def getSymbol(self,symbol_id=None):
        '''
        Fetches the deatail of symbol from the symbol relation.generates a list of dic for the Symbol Mapper
        & adds records to the table 
        


        Parameters
         ----------
        symbol_ids : list or str of symbols
            A list of stock symbols that conform to the Alpaca API request structure.
  
        Returns
        -------
        
       list of json objects if no argument or list of arguments is passsed

       else json object in list

            
        '''


        #create session

        


        session=self.Session()
        
        if symbol_id == None:

            symbols=session.query(Symbol).all()
            
        
        if type(symbol_id)==list:

            symbols=session.query(Symbol).filter(Symbol.ticker.in_(symbol_id)).all()
            
        

        if type(symbol_id)==str:
            
            symbols=session.query(Symbol).filter(Symbol.ticker == symbol_id).all()

        
        

        return json.dumps([object_as_dict(symbol) for symbol in symbols])

       


       


            



            



















            # print(json.dumps([dict(symbol) for symbol in symbols]))


































#         ofigi=OpenFigi()
#         


#         dfs=[pd.DataFrame.from_dict(job[0][1]["data"]) for job in jobs]


#         sdf=pd.concat(dfs)

#         compression_opts = dict(method='zip',
#                         archive_name='figi.csv')  
#         sdf.to_csv('figi.zip', index=False,
#           compression=compression_opts)  
      





        

# obj=SymbolController()


# obj.bulkInsertFromProviders("Alpaca")





