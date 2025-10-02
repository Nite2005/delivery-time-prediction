from fastapi import FastAPI
from app.api import routes_auth, routes_predict, routes_dashboard
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.exceptions import register_exception_handlers
from app.middleware.logging import LoggingMiddleware
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title = "Delivery Time Prediction API")

app.add_middleware(LoggingMiddleware)
app.include_router(routes_dashboard.router, tags=['Dashboard'])
app.include_router(routes_auth.router, tags=['Auth'])
app.include_router(routes_predict.router, tags=['Prediction'])

Instrumentator().instrument(app).expose(app)

register_exception_handlers(app)