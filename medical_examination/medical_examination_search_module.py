#-*- coding:utf-8 -*-
import json
from ast import literal_eval
import pprint
import requests as re
import xmltodict as xtd

import keys

with open('medical_examination/state_code_medical_examination.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

with open('medical_examination/city_code_medical_examination.txt','r',encoding='utf-8') as f:
    city = literal_eval(f.read())
'''

with open('state_code_medical_examination.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

with open('city_code_medical_examination.txt','r',encoding='utf-8') as f:
    city = literal_eval(f.read())
'''
examination_dict={'grenChrgTypeCd':'일반검진','ichkChrgTypeCd':'영유아검진','bcExmdChrgTypeCd':'유방암','ccExmdChrgTypeCd':'대장암','cvxcaExmdChrgTypeCd':'자궁경부암','lvcaExmdChrgTypeCd':'간암','mchkChrgTypeCd':'구강','stmcaExmdChrgTypeCd':'위암'}



def stateSearch(st_name):
    state_dict = {}
    index = 0
    url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?siDoCd={0}&ServiceKey={1}".format(state[st_name],
        keys.MEDICAL_EXAMINATION)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
        responseData = request.text
        rD = xtd.parse(responseData)# XML형식의 데이터를 dict형식으로 변환시켜줌
        rDJ = json.dumps(rD)# dict 형식의 데이터를 json형식으로 변환
        rDD = json.loads(rDJ)# json형식의 데이터를 dict 형식으로 변환

        totalCount = int(rDD["response"]["body"]["totalCount"])
        maxPage = (totalCount // 10) + 1

        for l in range(1,maxPage):
         url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?pageNo={0}&siDoCd={1}&ServiceKey={2}".format(l,state[st_name],keys.MEDICAL_EXAMINATION)
         request = re.get(url)
         rescode = request.status_code
         print(url)
         if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
            responseData = request.text
            rD = xtd.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
            rDJ = json.dumps(rD)  # dict 형식의 데이터를 json형식으로 변환
            rDD = json.loads(rDJ)  # json형식의 데이터를 dict 형식으로 변환

            w_data = rDD["response"]["body"]["items"]["item"]  # item에 포함된 data list

            temp = []
            # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
            if totalCount == 1:
                temp.append(w_data)
                w_data = temp

            for e in range(len(w_data)):
                examination_list = []
                for key in examination_dict:
                    if w_data[e][key] == '1': examination_list.append(examination_dict[key])
                    examination = ",".join(examination_list)
                if "hmcTelNo" in w_data[e]:
                    state_dict[str(index)] = {"orgnm": w_data[e]["hmcNm"], "orgEmn": examination,
                                             "orgTlno": w_data[e]["hmcTelNo"],
                                             "orgAddr": w_data[e]["locAddr"]}
                else:
                    state_dict[str(index)] = {"orgnm": w_data[e]["hmcNm"], "orgEmn": examination,
                                             "orgTlno": None, "orgAddr": w_data[e]["locAddr"]}
                index = index + 1
    return state_dict

def citySearch(st_name,ct_name):
    city_dict = {}
    index = 0
    url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?siDoCd={0}&siGunGuCd={1}&ServiceKey={2}".format(state[st_name],city[st_name][ct_name],keys.MEDICAL_EXAMINATION)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
        responseData = request.text
        rD = xtd.parse(responseData)# XML형식의 데이터를 dict형식으로 변환시켜줌
        rDJ = json.dumps(rD)# dict 형식의 데이터를 json형식으로 변환
        rDD = json.loads(rDJ)# json형식의 데이터를 dict 형식으로 변환

        totalCount = int(rDD["response"]["body"]["totalCount"])
        maxPage = (totalCount // 10) + 1

        for l in range(1,maxPage):
         url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?pageNo={0}&siDoCd={1}&siGunGuCd={2}&ServiceKey={3}".format(l,state[st_name],city[st_name][ct_name],keys.MEDICAL_EXAMINATION)
         request = re.get(url)
         rescode = request.status_code

         if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
            responseData = request.text
            rD = xtd.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
            rDJ = json.dumps(rD)  # dict 형식의 데이터를 json형식으로 변환
            rDD = json.loads(rDJ)  # json형식의 데이터를 dict 형식으로 변환

            w_data = rDD["response"]["body"]["items"]["item"]  # item에 포함된 data list

            temp = []
            # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
            if totalCount == 1:
                temp.append(w_data)
                w_data = temp

            for e in range(len(w_data)):
                examination_list = []
                for key in examination_dict:
                    if w_data[e][key] == '1': examination_list.append(examination_dict[key])
                    examination = ",".join(examination_list)
                if "hmcTelNo" in w_data[e]: city_dict[str(index)] = {"orgnm":w_data[e]["hmcNm"],"orgEmn":examination,
                                                                    "orgTlno":w_data[e]["hmcTelNo"],
                                                                     "orgAddr":w_data[e]["locAddr"]}
                else: city_dict[str(index)] = {"orgnm":w_data[e]["hmcNm"],"orgEmn":examination,
                                                "orgTlno":None, "orgAddr":w_data[e]["locAddr"]}
                index = index + 1
    return city_dict

def searchAll():
    key = []
    for s in state.keys():
        key.append(s)
    for k in key:
        result = stateSearch(str(k))
        return result
#전국 시/도 별 검색
#for key in state:
    #stateSearch(key)

#전국 구 별 검색
# for key in state:
#     for key2 in city:
        #citySearch(key,key2)

# result = citySearch('서울','종로구')
# pprint.pprint(result)

