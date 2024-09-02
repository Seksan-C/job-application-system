from sqlalchemy import Column, Integer, String
from .database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    address = Column(String)
    expected_salary = Column(Integer)
