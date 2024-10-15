# models.py

from sqlalchemy import Column, Integer, String, Date
from database import Base

class Message(Base):
    __tablename__ = "messages"  # This will create a table named "messages"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each record
    channel_title = Column(String, index=True)  # Channel Title
    channel_username = Column(String)  # Channel Username
    message_id = Column(String, unique=True)  # Unique Message ID
    message_text = Column(String)  # Message Text
    message_date = Column(Date)  # Date of the Message
    media_path = Column(String)  # Media Path
    message_length_category = Column(String)  # Length category of the message
