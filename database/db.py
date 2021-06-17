import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer,String,DateTime
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):
    __tablename__ ='tweets'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    uploader = Column(String,default='admin')
    created_on = Column(DateTime, default=datetime.now)
    prediction = Column(String,default="")

    def __str__(self):
        return self.filename

if __name__ == "__main__":
    engine = create_engine('sqlite:///database/db.sqlite3')
    Base.metadata.create_all(engine)