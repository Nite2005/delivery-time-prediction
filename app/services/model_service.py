import dagshub 
import mlflow
import joblib
import os
import json
import pandas as pd
from mlflow import MlflowClient
from app.core.config import settings
from app.db.models import User
from sqlalchemy.orm import Session
from app.db.models import PredictionLog
from app.cache.redis_cache import set_cached_prediction, get_cached_prediction
from app.core.data_clean_utils import perform_data_cleaning
from app.models.models import load_model, load_model_information, load_transformer, model_pipeline

dagshub_username = "Nite2005"
dagshub_token = os.getenv("DAGSHUB_TOKEN")
if not dagshub_token:
    raise EnvironmentError("DAGSHUB_TOKEN environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_username
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token
# dagshub.init(repo_owner='Nite2005', repo_name='delivery-time-prediction', mlflow=True)

# set the tracking server
dagshub_url = "https://dagshub.com"
repo_owner = "Nite2005"
repo_name = "delivery-time-prediction"
mlflow.set_tracking_uri(f"https://dagshub.com/{dagshub_username}/delivery-time-prediction.mlflow")
# dagshub.init(repo_owner='Nite2005', repo_name='delivery-time-prediction', mlflow=True)
# mlflow.set_tracking_uri("https://dagshub.com/Nite2005/delivery-time-prediction.mlflow")

client = MlflowClient()
run_information = load_model_information(settings.RUN_INFORMATION_PATH)

model = load_model(settings.RUN_INFORMATION_PATH, "Staging")



model_pipe = model_pipeline(settings.PREPROCESSOR_PATH,model)

def log_prediction(data: dict, prediction: float, db: Session, users_id:int):
    log = PredictionLog(
        user_id=users_id,
        input_data=json.dumps(data),
        prediction=prediction
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def predict_delivery_time(data: dict, db: Session, user_id: int):
    cache_key = " ".join([str(val) for val in data.values()])
    cached = get_cached_prediction(cache_key)
    if cached:
        return cached
    
    input_data = pd.DataFrame([data])
    # cleaned_data = perform_data_cleaning(input_data)
    prediction = model_pipe.predict(input_data)[0]
    log_prediction(data,prediction, db, user_id)
    set_cached_prediction(cache_key, prediction)
    return prediction