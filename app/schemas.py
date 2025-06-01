from pydantic import BaseModel

class TransactionInput(BaseModel):
    Transaction_Amount: float
    Transaction_Distance: float
    Card_Type: str
    Transaction_Type: str
    Device_Type: str
    Authentication_Method: str
    IP_Address_Flag: int
    Previous_Fraudulent_Activity: int
    Is_Weekend: int
    # Add other fields you retained during training

class PredictionOutput(BaseModel):
    prediction: str

# What is this schemas, pydantic etc??