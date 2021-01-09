from typing import Optional
from fastapi import FastAPI,Request,Form 
from fastapi.templating import Jinja2Templates


app=FastAPI()
templates=Jinja2Templates("templates")



@app.get("/")


async def get_index(request:Request):

    from Views import StockPriceController

    controller=StockPriceController.StockPriceController()

    stocks = controller.getDailyPrices() 

    return templates.TemplateResponse("index.html",{"request": request, "stocks":stocks})

    



