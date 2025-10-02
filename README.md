# Delivery Time Prediction API

> Predict delivery times for e-commerce orders using a reproducible ML pipeline and serve predictions via a FastAPI endpoint with full observability, authentication, and caching.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Architecture](#architecture)
* [Tech Stack](#tech-stack)
* [Prerequisites](#prerequisites)
* [Repository Layout](#repository-layout)
* [Quickstart — Run Locally](#quickstart--run-locally)
* [Data & DVC pipeline](#data--dvc-pipeline)
* [Training & MLflow](#training--mlflow)
* [Model Serving (FastAPI + JWT + Redis)](#model-serving-fastapi--jwt--redis)
* [Database Logging (SQLAlchemy)](#database-logging-sqlalchemy)
* [Testing (pytest)](#testing-pytest)
* [Docker](#docker)
* [Kubernetes Deployment](#kubernetes-deployment)
* [CI/CD](#cicd)
* [Monitoring (Prometheus & Grafana)](#monitoring-prometheus--grafana)
* [Environment variables](#environment-variables)
* [How to contribute](#how-to-contribute)
* [License](#license)

---

## Overview

This project contains an end-to-end machine learning application that predicts delivery time for orders. It includes:

* Reproducible data versioning with **DVC**
* Experiment tracking with **MLflow**
* Model training in Python (scikit-learn / your chosen framework)
* A production-ready inference API built with **FastAPI** and **Pydantic** for schema validation
* Authentication & authorization with **JWT tokens**
* Prediction & user logging with **SQLAlchemy + relational DB**
* Caching layer with **Redis** for low-latency predictions
* Monitoring with **Prometheus + Grafana**
* Unit & integration tests with **pytest**
* Containerization with **Docker** and deployment instructions for **Kubernetes**
* Example **CI/CD** (GitHub Actions) to automate tests, training, and deployment

## Features

* Trainable ML pipeline with configurable preprocessing
* Data version control (DVC) for datasets and model artifacts
* MLflow tracking server for experiments and model registry
* REST API to serve model predictions with JWT-secured endpoints
* SQLAlchemy ORM models for storing users, login sessions, and predictions
* Redis cache layer for repeat prediction requests
* Prometheus metrics endpoint for monitoring, Grafana dashboards for visualization
* CI/CD pipeline for automation

## Architecture

```
+-----------+   +--------+   +-----------+   +-----------+
| Raw Data  |-> |  DVC   |-> | Training  |-> |  MLflow   |
+-----------+   +--------+   +-----------+   +-----------+
                                         |
                                         v
                                   +-----------+
                                   | FastAPI   |
                                   | + JWT     |
                                   | + Redis   |
                                   +-----------+
                                         |
                                         v
                                   +-----------+
                                   | SQLAlchemy|
                                   |  logging  |
                                   +-----------+
                                         |
                                         v
                                +-------------------+
                                | Docker + K8s      |
                                +-------------------+
                                         |
                                         v
                             +-------------------------+
                             | Prometheus + Grafana    |
                             +-------------------------+
```

## Tech Stack

* Language: Python 3.10+
* ML: scikit-learn, pandas, numpy
* Experiment-Tracking: MLflow
* Data versioning: DVC
* API: FastAPI + Pydantic
* Authentication: JWT (PyJWT / FastAPI-JWT-Auth)
* Database: SQLAlchemy ORM
* Cache: Redis
* Monitoring: Prometheus + Grafana
* Testing: pytest
* Container: Docker
* Orchestration: Kubernetes (minikube / EKS)
* CI: GitHub Actions

## Repository Layout

```
├── README.md
├── data/
├── dvc.yaml
├── params.yaml
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── api/
│   │   ├── main.py          # FastAPI app
│   │   ├── auth.py          # JWT authentication
│   │   ├── cache.py         # Redis integration
│   │   └── db.py            # SQLAlchemy ORM
│   └── utils/
├── tests/
├── Dockerfile
├── k8s/
├── .github/workflows/
└── mlflow/
```

## Model Serving (FastAPI + JWT + Redis)

* JWT-based authentication for secure endpoints:

  * `POST /login` → returns JWT token
  * `POST /predict` → requires valid JWT
  * 

* Redis caching for predictions:

  * Before computing prediction, check Redis cache by hash of input features.
  * Store prediction in Redis for faster repeated queries.

## Database Logging (SQLAlchemy)

* Tables:

  * `users` → stores user credentials (hashed passwords)
  * `predictions` → logs input features, prediction result, timestamp, and user id

* Example SQLAlchemy model:

```python
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    features = Column(JSON)
    predicted_minutes = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Monitoring (Prometheus & Grafana)

* FastAPI exposes `/metrics` endpoint with Prometheus format using `prometheus-client`

* Key metrics:

  * request count & latency
  * cache hits/misses
  * prediction errors

* Prometheus scrapes metrics from API service

* Grafana visualizes dashboards for API performance and ML model monitoring

## Environment variables

| Name                | Purpose                    |
| ------------------- | -------------------------- |
| JWT_SECRET_KEY      | Secret key for JWT signing |
| DATABASE_URL        | SQLAlchemy database URL    |
| REDIS_URL           | Redis connection string    |
| MLFLOW_TRACKING_URI | MLflow tracking server     |
| DVC_REMOTE_URL      | DVC remote storage         |
| MODEL_PATH          | Model artifact path        |

---

This README now includes ML, Python, MLflow, DVC, CI/CD, FastAPI, Pydantic, pytest, Docker, Kubernetes, JWT authentication, SQLAlchemy for user & prediction logging, Redis caching, and Prometheus + Grafana monitoring.
