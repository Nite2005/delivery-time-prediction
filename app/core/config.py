import os
import joblib
from pathlib import Path
import json
from dotenv import load_dotenv

load_dotenv()

root_path = Path(__file__).parent.parent.parent


class Settings:
    PROJECT_NAME = 'Delivery Time Prediction'
    API_KEY = os.getenv('API_KEY','demo-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')
    JWT_ALGORITHM = 'HS256'
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    PREPROCESSOR_PATH =root_path / "models" / "preprocessor.joblib"
    RUN_INFORMATION_PATH = root_path / "run_information.json"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///C:/Users/hp/Desktop/delivery-time-prediction/sql_app.db")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
settings = Settings()
