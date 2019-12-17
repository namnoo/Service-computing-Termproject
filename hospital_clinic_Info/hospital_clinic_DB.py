import pandas as pd
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from antibiotics_Info import antibiotics_DB

engine = create_engine('sqlite:///hospital_clinic_Info.db', echo=False, connect_args={'check_same_thread': False}) #database 생성
Base = declarative_base()

class hospitalInfo(Base): # 병원 table 생성
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

    def json_all_hospitals(hospital):
        hospital_list = []

        for h in hospital:
            anti = antibiotics_DB.search_antibiontics_info(h.hospitalName, h.address)

            hospital_list.append({"hosnm" : h.hospitalName,
                             "hosTlno" : h.telNum,
                             "hosAddr" : h.address,
                             "hosType" : h.hospitalType,
                             "hosSubj" : h.medicalCourse,
                             "hosAnti" : anti})

        hospital_dict = {"result":
                             {"type": "병원",
                              "list": hospital_list}
                         }

        dictToJson = json.dumps(hospital_dict, ensure_ascii=False)

        return dictToJson


class clinicInfo(Base): # 의원 table
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

    def json_all_clinics(clinic):
        clinic_list = []

        for c in clinic:
            anti = antibiotics_DB.search_antibiontics_info(c.clinicName, c.address)

            clinic_list.append({"clinm" : c.clinicName,
                             "cliTlno" : c.telNum,
                             "cliAddr" : c.address,
                             "cliType" : c.clinicType,
                             "cliSubj" : c.medicalCourse,
                             "cliAnti" : anti})

        clinic_dict = {"result":
                             {"type": "의원",
                              "list": clinic_list}
                         }

        dictToJson = json.dumps(clinic_dict, ensure_ascii=False)

        return dictToJson

Base.metadata.create_all(engine)


file_name = ['hospital_clinic_Info/hospitalInfo.csv','hospital_clinic_Info/clinicInfo.csv']
table_name = [hospitalInfo.__tablename__,clinicInfo.__tablename__]
for i in range(2):
    anti_read = pd.read_csv(file_name[i])
    anti_read.to_sql(con=engine, index_label='no', name=table_name[i], if_exists='replace')

db_session = sessionmaker(bind=engine)
db_session = db_session()


def search_hostpital_state(st_name): # 시/도 단위 검색
    hospital = db_session.query(hospitalInfo).filter(hospitalInfo.address.like('%'+st_name+'%'))
    hospitalInfo.print_all_hospitals(hospital)

def search_hostpital_city(st_name,ct_name): # 시/구 단위 검색
    hospital = db_session.query(hospitalInfo).filter(
        hospitalInfo.address.like(st_name + ' ' + ct_name + '%'))

    return hospitalInfo.json_all_hospitals(hospital)


def search_clinic_state(st_name): # 시/도 단위 검색
    clinic = db_session.query(clinicInfo).filter(clinicInfo.address.like('%'+st_name+'%'))
    clinicInfo.print_all_clinics(clinic)

def search_clinic_city(st_name,ct_name): # 시/구 단위 검색
    clinic = db_session.query(clinicInfo).filter(
        clinicInfo.address.like(st_name + ' ' + ct_name + '%'))

    return clinicInfo.json_all_clinics(clinic)
