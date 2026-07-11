from pathlib import Path


PROJECT_ROOT=Path(__file__).resolve().parents[3]

MODEL_DIR=PROJECT_ROOT/"Model"
DATASET_DIR=PROJECT_ROOT/"Dataset"
LOG_DIR=PROJECT_ROOT/'LOG'

MODEL_PATH=MODEL_DIR/"used_phone_prediction.joblib"
DATASET_PATH=DATASET_DIR/"used_phone_price_prediction_1M.csv"


TRAINING_LOG_PATH=LOG_DIR/"training.log"
PREDICTION_LOG_PATH=LOG_DIR/"prediction.log"



HYPER_PARAMS_YAML_PATH = PROJECT_ROOT /"src" /"training"/ "config"/"hyper_params.yaml"
