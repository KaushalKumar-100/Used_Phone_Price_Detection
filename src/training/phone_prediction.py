import os
import logging
from dotenv import load_dotenv
from pathlib import Path

import yaml
from joblib import dump
from sklearn.ensemble import HistGradientBoostingRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    root_mean_squared_error,
    mean_absolute_error,
    r2_score
)

load_dotenv()

RANDOM_STATE=int(os.getenv("RANDOM_STATE"))
TEST_SIZE=float(os.getenv("TEST_SIZE"))
N_SPLIT=int(os.getenv("N_SPLIT"))
TARGET_COLS=os.getenv("TARGET_COLS")

PROJECT_DIR=Path(os.getenv("PROJECT_ROOT")).resolve()


DATASET=(PROJECT_DIR
         / os.getenv('DATASET_DIR')
         )

DATASET_PATH=(DATASET
              / os.getenv('DATASET_PATH')
              )

MODEL_DIR=(PROJECT_DIR
           / os.getenv("MODEL_DIR")
           )
MODEL_PATH=(MODEL_DIR
            / os.getenv("MODEL_PATH")
            )
LOG_DIR=(PROJECT_DIR
         /os.getenv("LOG_DIR")
         )


LOG_PATH_TRAINING=(LOG_DIR
                  / os.getenv("LOG_PATH_TRAINING")
                  )


HYPER_PARAMS_YAML_PATH=(PROJECT_DIR
                   / os.getenv("HYPER_PARAMS_YAML_PATH")
                   )

LOG_DIR.mkdir(parents=True,exist_ok=True)
MODEL_DIR.mkdir(parents=True,exist_ok=True)
LOG_PATH_TRAINING.parent.mkdir(parents=True,exist_ok=True)


def used_phone_prediction():
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(LOG_PATH_TRAINING)
            ]
         )
        
        df=pd.read_csv(DATASET_PATH)
        logging.info(f"Dataset has been read by df {df.shape}")
        
        sample_size=min(len(df),N_SPLIT)
        
        new_df=df.sample(n=sample_size,random_state=RANDOM_STATE)
        X=new_df.drop(columns=[TARGET_COLS,'city_tier','seller_type'])
        y=new_df[TARGET_COLS]
        
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=TEST_SIZE,random_state=RANDOM_STATE)
        logging.info(f"train and test data splited {X_train.shape} and {X_test.shape}")
        
        with open(HYPER_PARAMS_YAML_PATH,'r') as file:
            hyperparams=yaml.safe_load(file)
            
        model_params=hyperparams['used_phone_prediction']['params']
        best_model=HistGradientBoostingRegressor(**model_params,random_state=RANDOM_STATE)
        if 'used_phone_prediction' not in hyperparams:
            raise ValueError("Not in Configuration:")
        
        cat_cols=['brand',
                'model',
                'release_year',
                'ram_gb',
                'storage_gb',
                'os_type',
                'has_5g',
                'purchase_year',
                'condition',
                'screen_cracked',
                'body_damage',
                'repair_history',
                'water_damage',
                'box_available',
                'charger_available']
        
        nums_cols=['screen_size_inches',
                    'battery_capacity',
                    'processor_score',
                    'camera_score',
                    'original_price',
                    'age_months',
                    'usage_hours_per_day',
                    'battery_health',
                    'warranty_remaining_months',
                    'market_demand_score']           
        
        nums_pipe=Pipeline(
            steps=[
                ("scaler",StandardScaler()),   
            ]
        )
        cat_pipe=Pipeline(
            steps=[
                ('oe',OrdinalEncoder(handle_unknown='use_encoded_value',
                                     unknown_value=-1))
            ]
        )
        preprocess=ColumnTransformer(
            transformers=[
                ('num',nums_pipe,nums_cols),
                ('cat',cat_pipe,cat_cols)
            ]
        )
        best_fit_pipeline=Pipeline(
            steps=[
                ('preprocess',preprocess),
                ('model',best_model)
            ]
        )
        
        best_fit_pipeline.fit(X_train,y_train)
        logging.info("Model training completed")
        
        
        y_train_pred=best_fit_pipeline.predict(X_train)
        y_test_pred=best_fit_pipeline.predict(X_test)
        
        
        y_train_rmse=root_mean_squared_error(y_train,y_train_pred)
        y_test_rmse=root_mean_squared_error(y_test,y_test_pred)
        
        y_train_mae=mean_absolute_error(y_train,y_train_pred)
        y_test_mae=mean_absolute_error(y_test,y_test_pred)
        
        
        y_train_r2=r2_score(y_train,y_train_pred)
        y_test_r2=r2_score(y_test,y_test_pred)
        
        
        logging.info(f"training rmse: {y_train_rmse}")
        logging.info(f"test rmse: {y_test_rmse}")
        
        
        logging.info(f"training mae: {y_train_mae}")
        logging.info(f"test mae: {y_test_mae}")
        
        
        logging.info(f"training r2: {y_train_r2}")
        logging.info(f"test r2: {y_test_r2}")
    
        
        
        dump(best_fit_pipeline,MODEL_PATH)
        logging.info(f"model saved to {MODEL_PATH}")
        logging.info('Model training completed')
        
        
        
             
        
        
        
    except Exception as e:
       
        logging.exception(f"Training failed {e}")
    


if __name__=="__main__":
    used_phone_prediction()
