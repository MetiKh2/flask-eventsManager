from db_manager import db
from sqlalchemy import Integer, Text, DateTime, Time, Column, Boolean, String
from datetime import datetime


class Event(db.Model):
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String)
    title = Column(String)
    price = Column(Integer)
    holding_at = Column(DateTime())
    time = Column(String())
    url = Column(String())
    image = Column(String())
    address = Column(String())
    description = Column(Text())
    phone = Column(String())
    created_at = Column(DateTime(), default=datetime.now())
    published = Column(Boolean(), default=False)
