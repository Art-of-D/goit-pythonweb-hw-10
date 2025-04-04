from sqlalchemy import  Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import Optional

Base = declarative_base()

class Contact(Base):
  __tablename__ = "contacts"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  surname = Column(String, nullable=False)
  email = Column(String, nullable=False)
  phone = Column(String, nullable=False)
  birthdate = Column(Date, default=datetime.date)
  notes: Optional[str] = Column(String, nullable=True)
  