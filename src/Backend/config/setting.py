from pydantic_settings import BaseSettings


class settings (BaseSettings):
    log_path=str
    model_path=str
    
    
    class Config:
        env_file='.env'
        env_file_encoding='utf-8'
        extra='allow'
