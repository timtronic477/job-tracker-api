from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from database import get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class JobApplicationCreate(BaseModel):
    company: str
    position: str
    status: str = "applied"
    notes: Optional[str] = None


class JobApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    position: str
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


@app.get("/")
def read_root():
    return {"message": "Job Tracker API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}




@app.get("/applications/active", response_model=list[JobApplicationResponse])
def get_active_applications(db: Session = Depends(get_db)):
    active_apps = db.query(models.Application).filter(
        models.Application.status.in_(['applied', 'interviewing'])
    ).all()
    return active_apps


@app.get('/applications/stats')
def get_stats(db: Session = Depends(get_db)):
    total = db.query(models.Application).count()

    if total == 0:
        return {'total': 0, 'offers': 0, 'acceptance_rate': 0.0}
    offers = db.query(models.Application).filter(
        models.Application.status == 'offer'
    ).count()

    acceptance_rate = offers/total

    return {
        "total_applications": total,
        "total_offers": offers,
        "acceptance_rate": acceptance_rate
    }


@app.get('/applications/search', response_model=list[JobApplicationResponse])
def search_application(query: str, db: Session = Depends(get_db)):
    search_pattern = f"%{query}"

    results = db.query(models.Application).filter(
        (models.Application.company.ilike(search_pattern)) |
        (models.Application.position.ilike(search_pattern))
    )
    return results

@app.get('/applications/recent', response_model=list[JobApplicationResponse])
def get_recent_application(days: int = 7, db: Session = Depends(get_db)):

    cutoff_date = datetime.now() - timedelta(days=days)

    results = db.query(models.Application).filter(
        models.Application.created_at >= cutoff_date
    ).order_by(models.Application.created_at.desc()).all()

    return results

@app.get("/applications/{application_id}", response_model=JobApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@app.get("/applications", response_model=list[JobApplicationResponse])
def get_applications(sort_by: str = 'created_at', order: str = 'desc', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    sort_options = {
        'created_at': models.Application.created_at,
        'company': models.Application.company,
        'position': models.Application.position,
        'status': models.Application.status
    }

    sort_column = sort_options.get(sort_by, models.Application.created_at)

    query = db.query(models.Application)
    if order == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(skip).limit(limit)

    return query.all()


@app.post("/applications", response_model=JobApplicationResponse)
def create_application(application: JobApplicationCreate, db: Session = Depends(get_db)):
    db_application = models.Application(
        company=application.company,
        position=application.position,
        status=application.status,
        notes=application.notes
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@app.put("/applications/{application_id}", response_model=JobApplicationResponse)
def update_application(
        application_id: int,
        application_update: JobApplicationUpdate,
        db: Session = Depends(get_db)
):
    db_application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")

    update_data = application_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)

    return db_application

@app.delete('/applications/{application_id}')
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()

    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_application)
    db.commit()

    return {'message': 'Application deleted successfully', 'id': application_id}
