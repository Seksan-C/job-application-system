from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
import csv
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import csv
import io
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud, models, schemas

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # คุณสามารถระบุโดเมนที่อนุญาตได้ เช่น ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],  # สามารถระบุเฉพาะ methods ที่ต้องการอนุญาต เช่น ["GET", "POST"]
    allow_headers=["*"],  # สามารถระบุเฉพาะ headers ที่ต้องการอนุญาตได้
)

@app.post("/applications/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(database.get_db)):
    return crud.create_application(db=db, application=application)

@app.get("/applications/", response_model=list[schemas.Application])
def read_applications(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_applications(db=db, skip=skip, limit=limit)

@app.get("/applications/{application_id}", response_model=schemas.Application)
def read_application(application_id: int, db: Session = Depends(database.get_db)):
    db_application = crud.get_application(db=db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@app.put("/applications/{application_id}", response_model=schemas.Application)
def update_application(application_id: int, application: schemas.ApplicationCreate, db: Session = Depends(database.get_db)):
    db_application = crud.update_application(db=db, application_id=application_id, application=application)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@app.delete("/applications/{application_id}", response_model=schemas.Application)
def delete_application(application_id: int, db: Session = Depends(database.get_db)):
    db_application = crud.delete_application(db=db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@app.get("/export/")
def export_applications(db: Session = Depends(database.get_db)):
    import pandas as pd
    query = db.query(models.Application).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "First Name", "Last Name", "Address", "Expected Salary"])  # ชื่อคอลัมน์

    for application in query:
        writer.writerow([
            application.id,
            application.first_name,
            application.last_name,
            application.address,
            application.expected_salary
        ])

    output.seek(0)  # เลื่อน cursor กลับไปจุดเริ่มต้นของไฟล์

    # ส่งออกไฟล์ CSV
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=applications.csv"})

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File format not supported")

    content = await file.read()
    csv_reader = csv.reader(io.StringIO(content.decode("utf-8")))
    
    header = next(csv_reader)
    for row in csv_reader:
        if len(row) != len(header):
            continue  # skip bad rows
        data_dict = dict(zip(header, row))
        
        # Assuming you have a schema `JobApplicationCreate` and a CRUD function to create the entry
        application_data = schemas.ApplicationCreate(**data_dict)
        crud.create_application(db, application_data)

    return JSONResponse(status_code=200, content={"message": "File processed successfully"})
