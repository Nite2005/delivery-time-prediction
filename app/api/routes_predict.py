from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.dependencies import get_api_key, get_current_user
from app.services.model_service import predict_delivery_time


router = APIRouter()


class Data(BaseModel):  
    ID: str
    Delivery_person_ID: str
    Delivery_person_Age: str
    Delivery_person_Ratings: str
    Restaurant_latitude: float
    Restaurant_longitude: float
    Delivery_location_latitude: float
    Delivery_location_longitude: float
    Order_Date: str
    Time_Orderd: str
    Time_Order_picked: str
    Weatherconditions: str
    Road_traffic_density: str
    Vehicle_condition: int
    Type_of_order: str
    Type_of_vehicle: str
    multiple_deliveries: str
    Festival: str
    City: str


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

@router.post('/predict')
def predict_price(data: Data, user=Depends(get_current_user),_=Depends(get_api_key)):
    prediction = predict_delivery_time(data.model_dump())
    return {'predicted_time':f'{prediction:,.2f}'}