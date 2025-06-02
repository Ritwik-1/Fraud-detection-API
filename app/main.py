from app.schemas import TransactionInput, PredictionOutput
from app.model import predict 
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_model = PredictionOutput)
def get_prediction(transaction: TransactionInput):
    result = predict(transaction)
    print("Log : ",result)
    return {"prediction":result}


# endpoints: 
# predict : post, gives data to server and takes results  
# root : just gets a message from server that it up running 


# What is this app.schemas and app.model?????
