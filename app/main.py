from fastapi import FastAPI 
from app.schemas import TransactionInput, PredictionOutput
from app.model import load_model, predict 

app = FastAPI()
model = load_model()

@app.get("/")
def read_root():
    return {"message":"Fraud Detection API is live"}

@app.post("/predict", response_model = PredictionOutput)
    def get_prediction(transaction: TransactionInput):
        result = predict(model,transaction)

        return {"prediction":result}


# endpoints: 
# predict : post, gives data to server and takes results  
# root : just gets a message from server that it up running 


# What is this app.schemas and app.model?????
