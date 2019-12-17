import pandas as pd
from sqlalchemy import Column, Integer
from sqlalchemy import create_engine, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///antibioticsInfo.db', echo=False, connect_args={'check_same_thread': False}) # database 생성
Base = declarative_base()

class antibioticsInfo(Base): # 항생제 table 생성
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

    def json_all_antibiotics(antibiotics):
        antibiotics_dict = {}
        index = 0
        for a in antibiotics:
            antibiotics_dict[str(index)] = {"antinm" : a.hospitalName,
                             "antiTlno" : a.evaluation,
                             "antiAddr" : a.address}
            index += 1

        return antibiotics_dict


Base.metadata.create_all(engine)

file_name = 'antibiotics_Info/antibiotics.csv'
anti_read = pd.read_csv(file_name)
anti_read.to_sql(con=engine, index_label='no', name=antibioticsInfo.__tablename__, if_exists='replace')

db_session = sessionmaker(bind=engine)
db_session = db_session()

def search_antibiotics_state(st_name): # 시/도 단위로 search
    antibiotics = db_session.query(antibioticsInfo).filter(antibioticsInfo.address.like('%'+st_name+'%'))
    antibioticsInfo.print_all_antibiotics(antibiotics)

def search_antibiotics_city(st_name,ct_name): # 시/구 단위로 search
    antibiotics = db_session.query(antibioticsInfo).filter(
        antibioticsInfo.address.like('%' + st_name + '%' and '%' + ct_name + '%'))

    return antibioticsInfo.json_all_antibiotics(antibiotics)

def search_antibiontics_info(name, address): # 병원 이름과 주소로 항생제 등급 평가 반환
    for user in db_session.query(antibioticsInfo).filter(antibioticsInfo.hospitalName==name).filter(antibioticsInfo.address==address):
        return user.evaluation
