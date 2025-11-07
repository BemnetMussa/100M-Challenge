from fastapi import FastAPI, Depends
import models
from database import engine, get_db
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
import time

models.Base.metadata.create_all(bind=engine) # based on our model create table

app = FastAPI()
# enable CORS for all origins (adjust allow_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def _calculate_analytics_summary(db):
    
    start_time = time.time()
    # calculate the top 5 most frequent event names
    summary_query = (
        db.query(
            models.Event.event_name,
            func.count(models.Event.id).label("event_count")
        )
        .group_by(models.Event.event_name)
        .order_by(func.count(models.Event.id).desc())
        .limit(5)
    )
    results = summary_query.all()
    end_time = time.time()
    duration = (end_time - start_time) * 1000 # in milliseconds

    # convert the results to a more JSON-friendly format
    summary_query = [
        {"event_name": name, "count": count} for name, count in results
    ]

    return summary_query, round(duration, 2)

@app.get("/")
def read_root():
    return {"message": "Database table are ready!!!"}

@app.get("/users/{user_id}/events")
def get_events_for_user(user_id: uuid.UUID, db: Session=Depends(get_db)):
    # fetch all events for specific user
    events = db.query(models.Event).filter(models.Event.user_id == user_id).all()
    return events

@app.get("/analytics/events/summary")
def get_event_summary(db: Session=Depends(get_db)):
    analytics_data, analytics_time_ms = _calculate_analytics_summary(db)

    return {
        "data": analytics_data,
        "query_time_ms": analytics_time_ms
    }
  
@app.get("/dashboard/data")
def get_dashboard_data(db: Session = Depends(get_db)):
    analytics_data, analytics_time_ms = _calculate_analytics_summary(db)

    response_data = {
        "dataset_size": 20_000_000,
        "load_time_minutes": 109,
        "performance":{
            "simple_query": {
                "before_ms": -1, # -1 represent Timeout
                "after_ms": 0.589
            },
            "analytics_query": {
                "before_ms":analytics_time_ms,
                "after_ms": None
            }
        },
        "analytics_summary":{
            "data": analytics_data,
            "query_time_ms": analytics_time_ms
        }
    }

    return response_data