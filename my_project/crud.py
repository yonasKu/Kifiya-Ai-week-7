# crud.py

from sqlalchemy.orm import Session
from models import Message
from schemas import MessageCreate, MessageResponse  # Assuming you have created schemas

def create_message(db: Session, message: MessageCreate):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: str):
    return db.query(Message).filter(Message.message_id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Message).offset(skip).limit(limit).all()

def delete_message(db: Session, message_id: str):
    db_message = db.query(Message).filter(Message.message_id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message
