# imports 


import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import alpaca_trade_api as Api
import config as Config



"""
|--------------------------------------------------------------------------------------------|
|                                                                                            |
|                                                                                            |
|        THIS CLASS iMPLEMENTS THE WRAPPER FOR ALPACA DATA PROVIDER IMPLEMENTED USING ALPACA | 
|        API....                                                                                   |
|                                                                                            |
|--------------------------------------------------------------------------------------------|

"""






class Alpaca:
   


    def __init__(self):

        #class properties 

        self.key=Config.ALPACA_API_KEY 
        self.secret=Config.ALPACA_SECRET_KEY
        self.url=Config.ALPACA_API_URL

        """
        ------------------------------------------------------------------------------------------------------------

                          Create connection with the alpaca server
   
         ------------------------------------------------------------------------------------------------------------
   
        """


    def connect(self):


        try:
            self.connection=Api.REST(self.key,self.secret,self.url)
            print("Connection Established With Provider") 
        except Exception as e:

            print("Error Connecting to Provider")
            raise e

   


         
        """
        ------------------------------------------------------------------------------------------------------------

            Retreives The List Of Stocks With Their Symbols,Name and Other Details 
   
        ------------------------------------------------------------------------------------------------------------

        """





    def getAssetList(self):
        
        try:
            account_info=self.connection.get_account()

            if account_info.status=="ACTIVE":
                self.assetList=self.connection.list_assets()
                return self.assetList

            
        except Exception as e:
            raise e

         

        """
        ------------------------------------------------------------------------------------------------------------

            Retreives The  Stock_prices  
   
        ------------------------------------------------------------------------------------------------------------

        """
            


    def getStockPrices(self,symbols=None,timeframe='1D',start=None,end=None,limit=None):
        if symbols==None :
            import Helper.helpers as Helper
            self.getAssetList()
            symbol_list=[getattr(asset,"symbol") for asset in self.assetList]
            stock_list=list(Helper.divide_chunks(symbol_list,50))
        else:
            stock_list=symbols

        try:
          stock_prices_df=[self.connection.get_barset(symbols,timeframe=timeframe,limit=limit,start=start,end=end).df for symbols in stock_list]

          return stock_prices_df

        except Exception as e:
            raise e



            









obj=Alpaca()
obj.connect()
prices=obj.getStockPrices(["AAPL","XOM"])
print(prices[0].head())






       


