import pytz
import sqlalchemy
from sqlalchemy import create_engine, and_, or_, Unicode, DateTime, Boolean
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///pharmacy_store_Info.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()

class pharmacyInfo(Base):
    __tablename__ = 'pharmacy'

    no = Column(Integer, primary_key=True)
    pharmacyName = Column(Unicode(128))
    telNum = Column(String)
    address = Column(Unicode(128))

class storeInfo(Base):
    __tablename__ = 'store'

    no = Column(Integer, primary_key=True)
    storeName = Column(Unicode(128))
    telNum = Column(String)
    address = Column(Unicode(128))


Base.metadata.create_all(engine)


file_name = ['pharmacyInfo.csv','storeInfo.csv']
table_name = [pharmacyInfo.__tablename__,storeInfo.__tablename__]
for i in range(2):
    anti_read = pd.read_csv(file_name[i])
    anti_read.to_sql(con=engine, index_label='no', name=table_name[i], if_exists='replace')


