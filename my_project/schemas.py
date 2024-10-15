# schemas.py

from pydantic import BaseModel
from datetime import date

class MessageBase(BaseModel):
    channel_title: str
    channel_username: str
    message_id: str
    message_text: str
    message_date: date
    media_path: str
    message_length_category: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int

    class Config:
        orm_mode = True  # This allows compatibility with SQLAlchemy models
