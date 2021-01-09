

"""
Set up the project with initial commits and data population processes

"""

from Views import StockPriceController,SymbolController,VendorController,FigiController

import config



def populates_prices_daily():
    stk_obj=StockPriceController.StockPriceController()



    
    stk_obj.hist_stock_pri_pvd('Alpaca', "day",stock_symbol=["APPL","MSFT"],price_type="daily",historical=True)
    


    print("daily stock prices added.....")



def populates_prices_intraday():
    stk_obj=StockPriceController.StockPriceController()



    
    stk_obj.hist_stock_pri_pvd('Alpaca', "day",stock_symbol=["APPL","MSFT"],price_type="1Min",historical=True)
    


    print("daily stock prices added.....")



def populate_vendors():
    ven_obj=VendorController.VendorController()
    vendors=[{
        "name":"Alpaca",
        "vendor_id":config.ALPACA_SECRET_KEY},
   
        {"name":"openfigi",
        "vendor_id":config.OPEN_FIGI_KEY},
    
        {"name":"Alphavantage",
        "vendor_id":config.ALPHAVANTAGE_KEY}]


    ven_obj.addVendor(vendors)



    print("Vendors added..............")




def populate_symbols():

    sym_obj=SymbolController.SymbolController()

    sym_obj.bulkInsertFromProviders("Alpaca")

    print("symbols added")



def populate_figi():
    obj=FigiController.figiController()

    obj.populate_figi_table()









populate_vendors()
populate_symbols()

populates_prices_daily()
populates_prices_intraday()
populate_figi()




















  

