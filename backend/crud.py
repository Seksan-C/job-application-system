from sqlalchemy.orm import Session
from . import models, schemas
import csv

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_applications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Application).offset(skip).limit(limit).all()

def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def update_application(db: Session, application_id: int, application: schemas.ApplicationCreate):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application:
        for key, value in application.dict().items():
            setattr(db_application, key, value)
        db.commit()
        db.refresh(db_application)
    return db_application

def delete_application(db: Session, application_id: int):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application:
        db.delete(db_application)
        db.commit()
    return db_application

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(
        first_name=application.first_name,
        last_name=application.last_name,
        address=application.address,
        expected_salary=application.expected_salary
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application
