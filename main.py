from fastapi import FastAPI, Depends
import models
from database import engine, get_db
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

models.Base.metadata.create_all(bind=engine) # based on our model create table

app = FastAPI()

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

    # convert the results to a more JSON-friendly format
    summary_query = [
        {"event_name": name, "count": count} for name, count in results
    ]

    return summary_query