import pytest
import mlflow
from mlflow import MlflowClient
import dagshub
import mlflow.sklearn
import lightgbm
import json
from pathlib import Path
import os
# dagshub.init(repo_owner='Nite2005', repo_name='delivery-time-prediction')

# # set the mlflow tracking server
# mlflow.set_tracking_uri("https://dagshub.com/Nite2005/delivery-time-prediction.mlflow")


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




def load_model_information(file_path):
    with open(file_path) as f:
        run_info = json.load(f)
        
    return run_info

file_path = Path(__file__).parent.parent / "run_information.json"

# set model name
model_name = load_model_information(file_path)["model_name"]



@pytest.mark.parametrize(argnames="model_name, stage",
                         argvalues=[(model_name, "Production")])
def test_load_model_from_registry(model_name,stage):
    client = MlflowClient()
    latest_versions = client.get_latest_versions(name=model_name,stages=[stage])
    latest_version = latest_versions[0].version if latest_versions else None
    
    assert latest_version is not None, f"No model at {stage} stage"
    
    # load the model
    model_path = f"models:/{model_name}/{stage}"

    # load the latest model from model registry
    model = mlflow.sklearn.load_model(model_path)
    
    assert model is not None, "Failed to load model from registry"
    print(f"The {model_name} model with version {latest_version} was loaded successfully")
    