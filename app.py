from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.pipeline import Pipeline
import uvicorn
import pandas as pd
import mlflow
import json
import joblib
from mlflow import MlflowClient
from sklearn import set_config
from scripts.data_clean_utils import perform_data_cleaning


set_config(transform_output="pandas")

import dagshub
import mlflow.client

dagshub.init(repo_owner='Nite2005', repo_name='delivery-time-prediction')

# set the mlflow tracking server
mlflow.set_tracking_uri("https://dagshub.com/Nite2005/delivery-time-prediction.mlflow")


class Data(BaseModel):
    age: float
    ratings: float
    weather: str
    traffic: str
    vehicle_condition: int
    type_of_order: str
    type_of_vehicle: str
    multiple_deliveries: float
    festival: str
    city_type: str
    is_weekend: int
    pickup_time_minutes: float
    order_time_of_day: str
    distance: float
    

