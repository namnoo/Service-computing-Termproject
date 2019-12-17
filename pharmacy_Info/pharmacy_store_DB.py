import pandas as pd
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

engine = create_engine('sqlite:///pharmacy_store_Info.db', echo=False, connect_args={'check_same_thread': False}) # database 생성
Base = declarative_base()

class pharmacyInfo(Base): # 약국 table 생성
    __tablename__ = 'pharmacy'

    no = Column(Integer, primary_key=True)
    pharmacyName = Column(Unicode(128))
    telNum = Column(String)
    address = Column(Unicode(128))

    def print_all_pharmacies(pharmacy):
        for p in pharmacy:
            pharmacyInfo.print_pharmacy(p)

    def print_pharmacy(p):
        print("약국명: {0} \n전화번호: {1} \n주소: {2} \n".format(
            p.pharmacyName,
            p.telNum,
            p.address
        ))

    def json_all_pharmacies(pharmacy):
        pharmacy_list = []

        for p in pharmacy:
            pharmacy_list.append({"phanm" : p.pharmacyName,
                                  "phaTlno" : p.telNum,
                                  "phaAddr" : p.address})

        pharmacy_dict = {"result":
                             {"type": '약국',
                              "list": pharmacy_list}
                         }

        dictToJson = json.dumps(pharmacy_dict, ensure_ascii=False)

        return dictToJson

class storeInfo(Base): # 안전 상비 의약품 판매 업소 table 생성
    __tablename__ = 'store'

    no = Column(Integer, primary_key=True)
    storeName = Column(Unicode(128))
    telNum = Column(String)
    address = Column(Unicode(128))

    def print_all_stores(store):
        for s in store:
            storeInfo.print_store(s)

    def print_store(s):
        print("약국명: {0} \n전화번호: {1} \n주소: {2} \n".format(
            s.storeName,
            s.telNum,
            s.address
        ))

    def json_all_stores(store):
        store_list = []

        for s in store:
            store_list.append({"stonm" : s.storeName,
                               "stoTlno" : s.telNum,
                               "stoAddr" : s.address})

        store_dict = {"result":
                          {"type": '안전상비의약품 판매업소',
                           "list": store_list}
                      }

        dictToJson = json.dumps(store_dict, ensure_ascii=False)

        return dictToJson

Base.metadata.create_all(engine)


file_name = ['pharmacy_Info/pharmacyInfo.csv','pharmacy_Info/storeInfo.csv']
table_name = [pharmacyInfo.__tablename__,storeInfo.__tablename__]
for i in range(2):
    anti_read = pd.read_csv(file_name[i])
    anti_read.to_sql(con=engine, index_label='no', name=table_name[i], if_exists='replace')

db_session = sessionmaker(bind=engine)
db_session = db_session()


def search_pharmacy_state(st_name): # 시/도 단위로 search
    pharamacy = db_session.query(pharmacyInfo).filter(pharmacyInfo.address.like('%'+st_name+'%'))
    pharmacyInfo.print_all_pharmacies(pharamacy)

def search_pharmacy_city(st_name,ct_name): # 시/구 단위로 search
    pharmacy = db_session.query(pharmacyInfo).filter(
        pharmacyInfo.address.like(st_name + ' ' + ct_name + '%'))

    return pharmacyInfo.json_all_pharmacies(pharmacy)


def search_store_state(st_name): # 시/도 단위로 search
    store = db_session.query(storeInfo).filter(storeInfo.address.like('%'+st_name+'%'))
    storeInfo.print_all_stores(store)

def search_store_city(st_name, ct_name): # 시/구 단위로 search
    store = db_session.query(storeInfo).filter(
        storeInfo.address.like(st_name + ' ' + ct_name + '%'))

    return storeInfo.json_all_stores(store)
