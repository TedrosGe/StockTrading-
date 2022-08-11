
from http.client import HTTPException
from urllib.request import Request
from  fastapi import BackgroundTasks, FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from models import Stock
from database import SessionLocal, engine
from pydantic import BaseModel
import yfinance as yf
from schemas import StockRequest
# adding cors headers 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

models.Base.metadata.create_all(bind = engine)
templates = Jinja2Templates(directory= "template")
#adding cors url 
origins = [
    'http://localhost:3000'
]
#add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#establish db connection 
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def add_stock_data(id:int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    
    yf_data = yf.Ticker(stock.symbol)
    if yf_data is  None:
        raise HTTPException(status_code = 404, detail = "Symbol doesn't exist")
    stock.price = yf_data.info['previousClose']
    stock.forward_pe = yf_data.info['forwardPE']
    stock.forward_eps = yf_data.info['forwardEps']
    if yf_data.info['dividendYield'] is not None:
        stock.dividend_yield = int(yf_data.info['dividendYield']*100)
    db.add(stock)
    db.commit()
    return stock

def stock_graph():
    pass
    

@app.get("/home")
def home_page(request: Request, db: Session = Depends(get_db)):
    
    stocks = db.query(Stock).all()
    return stocks


@app.post("/stocks")
async def add_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    #add stock to db
    """
    adds new stock to db
    """
    stock = Stock()
    if stock_request.symbol in db.query(Stock.symbol):
        raise HTTPException(status_code = 404, detail= "Stock ALREADY In Inventory")

        
    yf_data = yf.Ticker(stock_request.symbol)     
    if "price"  not in yf_data.info:
        raise HTTPException(status_code = 404, detail = "Symbol doesn't exist")



    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()
    background_tasks.add_task(add_stock_data, stock.id)
    return {
        "code": "success",
        stock_request.symbol :"stock added "
    }
