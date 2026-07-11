from pydantic_settings import BaseSettings

class settings (BaseSettings):
    log_path=str,
    dataset_path=str,
    model_path=str,
    target_col=float,
    
    hyper_params_yaml_path=str,
    test_size=float,
    random_state=int
    
    