import os
import logging
from pathlib import Path
import sys
from pydantic import BaseModel
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))


import pandas as pd
from joblib import load

from src.Backend.config.path import (
MODEL_DIR,
DATASET_DIR,
LOG_DIR,
MODEL_PATH,
DATASET_PATH,
TRAINING_LOG_PATH,
PREDICTION_LOG_PATH,
HYPER_PARAMS_YAML_PATH

)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(PREDICTION_LOG_PATH),
        logging.StreamHandler()
    ]
)


logging.info("Loading Trained Model")
phone_model=load(MODEL_PATH)

logging.info("Model loaded successfully")



def predict_price(input_features):
    
    if isinstance(input_features,BaseModel):
        data=input_features.model_dump()
    elif isinstance(input_features,dict):
        data=input_features
        
    else:
        raise TypeError("input_features must be a dict or a pydantic model")
    
    X_df=pd.DataFrame([data])
    prediction=float(phone_model.predict(X_df)[0])
    
    
    logging.info(f"the model predicted the price:{prediction}")
    
    print(type(X_df))
    print(X_df)
    print(X_df.columns.tolist())
    return {
    "prediction": prediction
}




input_features = {
    'brand': 'Apple',
    'model': 'iPhone 13',
    'release_year': 2022,
    'ram_gb': 12,
    'storage_gb': 64,
    'screen_size_inches': 6.61,
    'battery_capacity': 3971,
    'processor_score': 73,
    'camera_score': 57,
    'os_type': 'iOS',
    'has_5g': 1,
    'original_price': 88762,
    'purchase_year': 2025,
    'age_months': 44,
    'usage_hours_per_day': 10.6,
    'condition': 'Good',
    'battery_health': 81,
    'screen_cracked': 0,
    'body_damage': 0,
    'repair_history': 0,
    'water_damage': 0,
    'warranty_remaining_months': 0,
    'box_available': 0,
    'charger_available': 1,
    'market_demand_score': 43
    
    }

value=predict_price(input_features)
print(value)
