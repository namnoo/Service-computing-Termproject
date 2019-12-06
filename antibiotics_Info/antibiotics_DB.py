import pandas as pd
from sqlalchemy import Column, Integer
from sqlalchemy import create_engine, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///antibioticsInfo.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()

class antibioticsInfo(Base):
    __tablename__ = 'antibiotics'

    no = Column(Integer, primary_key=True)
    hospitalName = Column(Unicode(128))
    evaluation = Column(Unicode(128))
    address = Column(Unicode(128))

    def print_all_antibiotics(antibiotics):
        for a in antibiotics:
            antibioticsInfo.print_antibiotics(a)

    def print_antibiotics(a):
        print("상호명: {0} \n등급: {1} \n주소: {2} \n".format(
            a.hospitalName,
            a.evaluation,
            a.address,
        ))

Base.metadata.create_all(engine)

file_name = 'antibiotics.csv'
anti_read = pd.read_csv(file_name)
anti_read.to_sql(con=engine, index_label='no', name=antibioticsInfo.__tablename__, if_exists='replace')

db_session = sessionmaker(bind=engine)
db_session = db_session()

def search_antibiotics_state(st_name):
    antibiotics = db_session.query(antibioticsInfo).filter(antibioticsInfo.address.like('%'+st_name+'%'))
    antibioticsInfo.print_all_antibiotics(antibiotics)

def search_antibiotics_city(st_name,ct_name):
    antibiotics = db_session.query(antibioticsInfo).filter(
        antibioticsInfo.address.like('%' + st_name + '%' and '%' + ct_name + '%'))
    antibioticsInfo.print_all_antibiotics(antibiotics)

search_antibiotics_state('천안시')
search_antibiotics_city('천안시','서북구')