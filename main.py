import os
import time
import uuid

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="100M Challenge API")

cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _calculate_analytics_summary(db: Session):
    start_time = time.time()

    results = (
        db.query(
            models.Event.event_name,
            func.count(models.Event.id).label("event_count"),
        )
        .group_by(models.Event.event_name)
        .order_by(func.count(models.Event.id).desc())
        .limit(5)
        .all()
    )

    duration_ms = (time.time() - start_time) * 1000

    summary = [
        {"event_name": name, "count": count} for name, count in results
    ]

    return summary, round(duration_ms, 2)


@app.get("/")
def read_root():
    return {"message": "Database tables are ready!"}


@app.get("/users/{user_id}/events")
def get_events_for_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    events = db.query(models.Event).filter(models.Event.user_id == user_id).all()
    return events


@app.get("/analytics/events/summary")
def get_event_summary(db: Session = Depends(get_db)):
    analytics_data, query_time_ms = _calculate_analytics_summary(db)
    return {
        "data": analytics_data,
        "query_time_ms": query_time_ms,
    }


@app.get("/dashboard/data")
def get_dashboard_data(db: Session = Depends(get_db)):
    analytics_data, query_time_ms = _calculate_analytics_summary(db)

    return {
        "dataset_size": 20_000_000,
        "load_time_minutes": 109,
        "performance": {
            "simple_query": {
                "before_ms": -1,
                "after_ms": 0.589,
            },
            "analytics_query": {
                "before_ms": query_time_ms,
                "after_ms": None,
            },
        },
        "analytics_summary": {
            "data": analytics_data,
            "query_time_ms": query_time_ms,
        },
    }
