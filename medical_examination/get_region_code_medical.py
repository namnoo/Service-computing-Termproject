#-*- coding:utf-8 -*-
import json
from ast import literal_eval

import requests as re
import xmltodict as xtd

import keys

with open('state_code_medical_examination.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

state_code_dict={}
city_code_dict={}

def state_code():
    url = "http://openapi1.nhis.or.kr/openapi/service/rest/CodeService/getSiDoList?ServiceKey={0}".format(keys.MEDICAL_REGION)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
        responseData = request.text
        rD = xtd.parse(responseData)# XML형식의 데이터를 dict형식으로 변환시켜줌
        rDJ = json.dumps(rD)# dict 형식의 데이터를 json형식으로 변환
        rDD = json.loads(rDJ)# json형식의 데이터를 dict 형식으로 변환

        totalCount = int(rDD["response"]["body"]["totalCount"])
        maxPage = (totalCount // 10) + 1

        for l in range(1,maxPage+1):
         url = "http://openapi1.nhis.or.kr/openapi/service/rest/CodeService/getSiDoList?pageNo={0}&ServiceKey={1}".format(l,keys.MEDICAL_REGION)
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
                code = w_data[e]["siDoCd"]
                name = w_data[e]["siDoNm"]
                state_code_dict[name] = code
    with open('state_code_medical_examination.txt', 'w', encoding='utf-8') as f:
        f.write(str(state_code_dict))
    print("state code is saved")

def city_code(st_name):
    city_code_dict[st_name] = {}
    url = "http://openapi1.nhis.or.kr/openapi/service/rest/CodeService/getSiGunGuList?pageNo=1&serviceKey={0}&siDoCd={1}".format(
        keys.MEDICAL_REGION,state[st_name])
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
        responseData = request.text
        rD = xtd.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
        rDJ = json.dumps(rD)  # dict 형식의 데이터를 json형식으로 변환
        rDD = json.loads(rDJ)  # json형식의 데이터를 dict 형식으로 변환

        totalCount = int(rDD["response"]["body"]["totalCount"])
        maxPage = (totalCount // 10) + 1

        for l in range(1, maxPage + 1):
            url = "http://openapi1.nhis.or.kr/openapi/service/rest/CodeService/getSiGunGuList?pageNo={0}&serviceKey={1}&siDoCd={2}".format(
                l, keys.MEDICAL_REGION,state[st_name])
            request = re.get(url)
            rescode = request.status_code

            if rescode == 500: #rescode가 500인 경우에는 200으로 응답할 때 까지 계속해서 반복
                while(rescode != 200):
                    url = "http://openapi1.nhis.or.kr/openapi/service/rest/CodeService/getSiGunGuList?pageNo={0}&serviceKey={1}&siDoCd={2}".format(
                        l, keys.MEDICAL_REGION, state[st_name])
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
                if totalCount % 10 == 1 and l == maxPage:
                    temp.append(w_data)
                    w_data = temp

                for e in range(len(w_data)):
                    code = w_data[e]["siGunGuCd"]
                    name = w_data[e]["siGunGuNm"]
                    if name == None : city_code_dict[st_name][st_name] = code #구가 없을 경우
                    else : city_code_dict[st_name][name] = code

    with open('city_code_medical_examination.txt', 'w', encoding='utf-8') as f:
        f.write(str(city_code_dict))
    print("city code is saved")


#시/도 코드 저장
state_code()

#모든 시/도의 구 코드 저장
for key in state:
    city_code(key)

