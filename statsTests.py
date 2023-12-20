from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Dict

# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/db_name" не забыть
SQLALCHEMY_DATABASE_URL = ""
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

class Statistic(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True, index=True)
    statistic_name = Column(String, index=True)
    parameters = Column(String)
    value = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class StatisticData(BaseModel):
    statistic_name: str
    parameters: Dict[str, str]
    value: int

@app.post("/add_statistic/")
def add_statistic(data: StatisticData):
    db_session = sessionmaker(bind=engine)
    db = db_session()
    statistic = Statistic(statistic_name=data.statistic_name, parameters=str(data.parameters), value=data.value)
    db.add(statistic)
    db.commit()
    db.refresh(statistic)
    return {"message": "Statistic added successfully"}

@app.get("/get_statistic/")
def get_statistic(statistic_name: str):
    db_session = sessionmaker(bind=engine)
    db = db_session()
    statistic = db.query(Statistic).filter(Statistic.statistic_name == statistic_name).first()
    if statistic is None:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return {
        "statistic_name": statistic.statistic_name,
        "parameters": statistic.parameters,
        "value": statistic.value
    }