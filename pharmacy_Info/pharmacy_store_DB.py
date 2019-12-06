import pandas as pd
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///pharmacy_store_Info.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()

class pharmacyInfo(Base):
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

class storeInfo(Base):
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
            s.storeNameName,
            s.telNum,
            s.address
        ))

Base.metadata.create_all(engine)


file_name = ['pharmacyInfo.csv','storeInfo.csv']
table_name = [pharmacyInfo.__tablename__,storeInfo.__tablename__]
for i in range(2):
    anti_read = pd.read_csv(file_name[i])
    anti_read.to_sql(con=engine, index_label='no', name=table_name[i], if_exists='replace')


db_session = sessionmaker(bind=engine)
db_session = db_session()

# select pharmacy

def search_pharmacy_state(st_name):
    pharamacy = db_session.query(pharmacyInfo).filter(pharmacyInfo.address.like('%'+st_name+'%'))
    pharmacyInfo.print_all_pharmacies(pharamacy)

def search_pharmacy_city(st_name,ct_name):
    pharmacy = db_session.query(pharmacyInfo).filter(
        pharmacyInfo.address.like('%' + st_name + '%' and '%' + ct_name + '%'))
    pharmacyInfo.print_all_pharmacies(pharmacy)

search_pharmacy_state('천안시')
search_pharmacy_city('천안시','동남구')

# select store

def search_store_state(st_name):
    store = db_session.query(storeInfo).filter(storeInfo.address.like('%'+st_name+'%'))
    storeInfo.print_all_stores(store)

def search_store_city(st_name, ct_name):
    store = db_session.query(storeInfo).filter(
        storeInfo.address.like('%' + st_name + '%' and '%' + ct_name + '%'))
    storeInfo.print_all_stores(store)

# search_store_state('천안시')
# search_store_city('천안시','동남구')