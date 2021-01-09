
"""

 ---------------------------------------------------------------------------------------------------------------------------
|                                                                                                                          |
|                                                                                                                          |
|              This is the Controller for performing CRUD and Logic operations on openfigi relation relationship.                 |                                                                      |                                                    |
|                                                                                                                          |
 --------------------------------------------------------------------------------------------------------------------------|



"""

import sys,os,time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config,json 
from sqlalchemy import create_engine,asc,desc
from sqlalchemy.orm import sessionmaker,Session

from Providers.Alpaca import Alpaca
from Providers.OpenFigi import OpenFigi
from datetime import date
from Helper.helpers import object_as_dict,divide_chunks
from Model.app_db import Symbol,Figi






class figiController:


    def __init__(self):
        self.url=config.DB_URL
        self.Session=sessionmaker()




    











#this function populates the figi_table



    def populate_figi_table(self):

        try:

            engine=create_engine(self.url)
            self.Session.configure(bind=engine)
            session=self.Session()
            symbols=session.query(Symbol.ticker).all()

        except Exception as e:

            raise e 


        finally:

            session.close()

        job_list=[{'idType': 'TICKER', 'idValue': symbol[0],} for symbol in symbols]

        
        
            


        




        chunked_job_list=divide_chunks(job_list,10)
       
        counter=0
        
        api=OpenFigi()

        

        for job in chunked_job_list:

            session=self.Session()

            if (counter+1) % 3==0:
                time.sleep(60)
            jobs=api.map_jobs(job)

            




            for item in jobs:
                if "data" in item.keys() and len(item["data"]) >= 11:
                    try:
                        session.bulk_insert_mappings(Figi,item["data"])
                    
                    except Exception as e:
                        raise e
            
                    finally:
                        session.commit()
                        
                    

                
                counter+=1








            # print(symbol_list)


            






