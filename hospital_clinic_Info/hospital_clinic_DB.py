import pandas as pd
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

    def print_all_hospitals(hospital):
        for h in hospital:
            hospitalInfo.print_hospital(h)

    def print_hospital(h):
        print("병원명: {0} \n전화번호: {1} \n주소: {2} \n병원종류: {3} \n진료과목: {4}\n".format(
            h.hospitalName,
            h.telNum,
            h.address,
            h.hospitalType,
            h.medicalCourse
        ))

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

    def print_all_clinics(clinic):
        for c in clinic:
            clinicInfo.print_clinic(c)

    def print_clinic(c):
        print("의원명: {0} \n전화번호: {1} \n주소: {2} \n의원종류: {3} \n진료과목: {4}\n".format(
            c.clinicName,
            c.telNum,
            c.address,
            c.clinicType,
            c.medicalCourse
        ))

Base.metadata.create_all(engine)


file_name = ['hospitalInfo.csv','clinicInfo.csv']
table_name = [hospitalInfo.__tablename__,clinicInfo.__tablename__]
for i in range(2):
    anti_read = pd.read_csv(file_name[i])
    anti_read.to_sql(con=engine, index_label='no', name=table_name[i], if_exists='replace')

db_session = sessionmaker(bind=engine)
db_session = db_session()

#select hospital

def search_hostpital_state(st_name):
    hospital = db_session.query(hospitalInfo).filter(hospitalInfo.address.like('%'+st_name+'%'))
    hospitalInfo.print_all_hospitals(hospital)

def search_hostpital_city(st_name,ct_name):
    hospital = db_session.query(hospitalInfo).filter(
        hospitalInfo.address.like('%' + st_name + '%' and '%' + ct_name + '%'))
    hospitalInfo.print_all_hospitals(hospital)

# search_hostpital_state('서울특별시')
# search_hostpital_city('서울특별시','강남구')

# select clinic

def search_clinic_state(st_name):
    clinic = db_session.query(clinicInfo).filter(clinicInfo.address.like('%'+st_name+'%'))
    clinicInfo.print_all_clinics(clinic)

def search_clinic_city(st_name,ct_name):
    clinic = db_session.query(clinicInfo).filter(
        clinicInfo.address.like('%' + st_name + '%' and '%' + ct_name + '%'))
    clinicInfo.print_all_clinics(clinic)

search_clinic_state('서울특별시')
search_clinic_city('서울특별시','강남구')