import pandas as pd
import requests
from pathlib import Path

# path for data
root_path = Path(__file__).parent.parent
data_path = root_path / "data" / "raw" / "swiggy.csv"

# prediction endpoint
predict_url = "http://127.0.0.1:8000/predict"

# sample row for testing the endpoint
sample_row = pd.read_csv(data_path).dropna().sample(1)
print("The target value is", sample_row.iloc[:,-1].values.item().replace("(min) ",""))
    
# remove the target column
data = sample_row.drop(columns=[sample_row.columns.tolist()[-1]]).squeeze().to_dict()
print(data)

headers = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1OTA1Mjk2N30.edsl9P9cGPvHh1j53Xinh6Yln4nhBmTHIhvZAzaF0w4",
    "api-key": "demo-key",
    "Content-Type": "application/json"
}

# get the response from API
response = requests.post(url=predict_url,json=data,headers=headers)

print("The status code for response is", response.status_code)
print("Error:", response.status_code, response.json())
if response.status_code == 200:
    print(f"The prediction value by the API is {response.text} min")
else:
    print("Error:", response.status_code)