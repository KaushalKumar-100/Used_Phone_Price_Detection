from fastapi import APIRouter

from src.Backend.schema.prediction_schema import (
    PredictionRequest,
    PredictionResponse
)

from src.Backend.service.predictor import predict_price


router=APIRouter()

@router.get("/status")
def api_check():
    return  {
        "status":"ok",
    }
    
@router.post("/price",response_model=PredictionResponse)
def predict_phone_price(input_features:PredictionRequest):
    
    result=predict_price(input_features)
    return PredictionResponse(**result)