import dagshub 
import mlflow
import joblib
import json
import pandas as pd
from mlflow import MlflowClient
from app.core.config import settings
from app.cache.redis_cache import set_cached_prediction, get_cached_prediction
from app.core.data_clean_utils import perform_data_cleaning
from app.models.models import load_model, load_model_information, load_transformer, model_pipeline

dagshub.init(repo_owner='Nite2005', repo_name='delivery-time-prediction')

# set the mlflow tracking server
mlflow.set_tracking_uri("https://dagshub.com/Nite2005/delivery-time-prediction.mlflow")


run_information = load_model_information(settings.RUN_INFORMATION_PATH)

model = load_model(settings.RUN_INFORMATION_PATH, "staging")



model_pipe = model_pipeline(settings.PREPROCESSOR_PATH,model)

def predict_delivery_time(data: dict):
    # cache_key = " ".join([str(val) for val in data.values()])
    # cached = get_cached_prediction(cache_key)
    # if cached:
    #     return cached
    
    input_data = pd.DataFrame([data])
    cleaned_data = perform_data_cleaning(input_data)
    prediction = model_pipe.predict(cleaned_data)[0]
    # set_cached_prediction(cache_key, prediction)
    return prediction