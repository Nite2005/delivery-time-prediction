FROM python:3.12-slim


RUN apt-get update && apt-get install -y libgomp1

WORKDIR /app

COPY requirements-dockers.txt ./


RUN pip install --no-cache-dir -r requirements-dockers.txt

COPY app ./app
COPY ./sql_app.db ./app/db/sql_app.db
COPY ./models/preprocessor.joblib ./models/preprocessor.joblib
COPY ./run_information.json ./


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
