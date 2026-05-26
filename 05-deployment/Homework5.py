import pickle
from pydantic import BaseModel
class Customer(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float


with open("/code/pipeline_v2.bin", 'rb') as f_in:
    pipeline = pickle.load(f_in)


from fastapi import FastAPI
import uvicorn

app = FastAPI(title = "convert")

customer = {
    "lead_source": "paid_ads",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0
}

def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)

@app.post("/predict")
def predict(customer: Customer):
    prob = predict_single(customer.dict())
    return {"convert_prob": prob,
            "convert": bool(prob >= 0.5)
            }
        
if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 1515)




