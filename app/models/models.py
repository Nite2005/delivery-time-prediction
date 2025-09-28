import joblib
import json 
import mlflow
import dagshub
from sklearn.pipeline import Pipeline
dagshub.init(repo_owner='Nite2005', repo_name='delivery-time-prediction')

# set the mlflow tracking server
mlflow.set_tracking_uri("https://dagshub.com/Nite2005/delivery-time-prediction.mlflow")

def load_model_information(file_path):
    with open(file_path,"r") as f:
        run_info = json.load(f)
        
    return run_info


def load_transformer(transformer_path):
    transformer = joblib.load(transformer_path)
    return transformer

def load_model(information_file_path,stage: str):
    model_name = load_model_information(information_file_path)['model_name']
    model_path = f"models:/{model_name}/{stage}"
    model = mlflow.sklearn.load_model(model_path)
    return model 

def model_pipeline(preprocessor_path: str,model):
    preprocessor = load_transformer(preprocessor_path)
    model_pipe = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ]
    )
    return model_pipe