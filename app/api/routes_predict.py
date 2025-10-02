from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.routes_auth import get_current_user
from app.services.model_service import predict_delivery_time
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.services.model_service import predict_delivery_time
from app.models.models import model_pipeline  # your ML pipeline

router = APIRouter()


class Data(BaseModel):  
  age:float
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
  pickup_time_minutes: int
  order_time_of_day: str
  distance: float
  distance_type: str


num_cols = ["age",
            "ratings",
            "pickup_time_minutes",
            "distance"]

nominal_cat_cols = ['weather',
                    'type_of_order',
                    'type_of_vehicle',
                    "festival",
                    "city_type",
                    "is_weekend",
                    "order_time_of_day"]

ordinal_cat_cols = ["traffic","distance_type"]

# @router.post('/predict')
# def predict_price(data: Data, user=Depends(get_current_user),_=Depends(get_api_key)):
#     prediction = predict_delivery_time(data.model_dump())
#     return {'predicted_time':f'{prediction:,.2f}'}

# @router.post("/predict")
# def predict(data: Data, db: Session = Depends(get_db), users:str=None):
#     prediction = predict_delivery_time(data, model_pipeline, db, users)
#     return {"prediction": prediction}
@router.post("/predict")
def predict(data: Data, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    - current_user automatically comes from JWT token
    - prediction logs can use current_user.id
    """
    prediction = predict_delivery_time(data.model_dump(), db, user_id=current_user.id)
    
    return {"prediction": prediction}
