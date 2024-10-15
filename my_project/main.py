# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas
import crud

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/messages/", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.get("/messages/{message_id}", response_model=schemas.MessageResponse)
def read_message(message_id: str, db: Session = Depends(get_db)):
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.get("/messages/", response_model=list[schemas.MessageResponse])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_messages(db, skip=skip, limit=limit)

@app.delete("/messages/{message_id}", response_model=schemas.MessageResponse)
def delete_message(message_id: str, db: Session = Depends(get_db)):
    db_message = crud.delete_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message
