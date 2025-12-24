from pydantic_settings import BaseSettings
from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    
    db_host:str
    db_port:int
    db_name:str
    db_pwd:str
    db_usr:str
    
    secret_key: str
    refresh_secret_key: str
    algorithm: str
    
    class Config:
        env_file=str(Path(__file__).parent.parent / ".env")
        print(f'environement created - {Path(Path(__file__).resolve().name)}')
        
        
setting = Settings()

print(setting.algorithm)