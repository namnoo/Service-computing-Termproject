import pytz
import sqlalchemy
from sqlalchemy import create_engine, and_, or_, Unicode, DateTime, Boolean
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///hospital_clinic_Info.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()

class hospitalInfo(Base):
    __tablename__ = 'hospital'

    no = Column(Integer, primary_key=True)
    hospitalName = Column(Unicode(128))
    telNum = Column(String)
    hospitalType = Column(Unicode(128))
    numDoc = Column(Integer)
    numRoom = Column(Integer)
    numBed = Column(Integer)
    medicalCourse = Column(Unicode(128))
    address = Column(Unicode(128))

class clinicInfo(Base):
    __tablename__ = 'clinic'

    no = Column(Integer, primary_key=True)
    clinicName = Column(Unicode(128))
    telNum = Column(String)
    clinicType = Column(Unicode(128))
    numDoc = Column(Integer)
    numRoom = Column(Integer)
    numBed = Column(Integer)
    medicalCourse = Column(Unicode(128))
    address = Column(Unicode(128))


Base.metadata.create_all(engine)


file_name = ['hospitalInfo.csv','clinicInfo.csv']
table_name = [hospitalInfo.__tablename__,clinicInfo.__tablename__]
for i in range(2):
    anti_read = pd.read_csv(file_name[i])
    anti_read.to_sql(con=engine, index_label='no', name=table_name[i], if_exists='replace')


