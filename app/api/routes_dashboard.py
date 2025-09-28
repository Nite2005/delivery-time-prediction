from fastapi import APIRouter


router = APIRouter()

@router.post('/')
def home():
    return {'message': 'Delivery Time Prediction API'}