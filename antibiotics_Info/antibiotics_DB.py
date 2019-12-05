import pytz
import sqlalchemy
from sqlalchemy import create_engine, and_, or_, Unicode, DateTime, Boolean
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///antibioticsInfo.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()

class antibioticsInfo(Base):
    __tablename__ = 'antibiotics'

    no = Column(Integer, primary_key=True)
    hospitalName = Column(Unicode(128))
    level = Column(Unicode(128))
    address = Column(Unicode(128))

Base.metadata.create_all(engine)

file_name = 'antibiotics.csv'
anti_read = pd.read_csv(file_name)
anti_read.to_sql(con=engine, index_label='no', name=antibioticsInfo.__tablename__, if_exists='replace')


