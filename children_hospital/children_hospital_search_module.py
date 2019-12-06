#-*- coding:utf-8 -*-
import requests as re
import xmltodict as xtd
import keys
import json
from ast import literal_eval
import sys
import io


with open('children_hospital/state_code_children_hospital.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

with open('children_hospital/city_code_children_hospital.txt','r',encoding='utf-8') as f:
    city = literal_eval(f.read())

def stateSearch(st_name):
    url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&serviceKey={2}".format(state[st_name],1,keys.CHILDREN_HOSPITAL)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
        responseData = request.text
        rD = xtd.parse(responseData)# XML형식의 데이터를 dict형식으로 변환시켜줌
        rDJ = json.dumps(rD)# dict 형식의 데이터를 json형식으로 변환
        rDD = json.loads(rDJ)# json형식의 데이터를 dict 형식으로 변환

        maxPage = int(rDD["response"]["body"]["maxPage"])

    for l in range(1,maxPage):
        url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&serviceKey={2}".format(
            state[st_name], l, keys.CHILDREN_HOSPITAL)
        request = re.get(url)
        rescode = request.status_code

        if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
            responseData = request.text
            rD = xtd.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
            rDJ = json.dumps(rD)  # dict 형식의 데이터를 json형식으로 변환
            rDD = json.loads(rDJ)  # json형식의 데이터를 dict 형식으로 변환

            w_data = rDD["response"]["body"]["items"]["item"]  # item에 포함된 data list
            total_count = int(rDD["response"]["body"]["totalCount"])  # 주어진 조건의 total count

            temp = []
            # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
            if total_count == 1:
                temp.append(w_data)
                w_data = temp

            # for e in range(len(w_data)):
            #     print()
            #     print('검진기관 :', w_data[e]["orgnm"])
            #     print('주소 :', w_data[e]["orgAddr"])
            #     print('전화번호 :', w_data[e]["orgTlno"])
            print()

def citySearch(st_name,ct_name):
    url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&sggCd={1}&pageNo={2}&numberOfRows=20&searchTpcd=ADDR&serviceKey={3}".format(
        state[st_name], city[st_name][ct_name], 1, keys.CHILDREN_HOSPITAL)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
        responseData = request.text
        rD = xtd.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
        rDJ = json.dumps(rD)  # dict 형식의 데이터를 json형식으로 변환
        rDD = json.loads(rDJ)  # json형식의 데이터를 dict 형식으로 변환

        maxPage = int(rDD["response"]["body"]["maxPage"])

    for l in range(1, maxPage):
        url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&sggCd={1}&pageNo={2}&numberOfRows=20&searchTpcd=ADDR&serviceKey={3}".format(
            state[st_name],city[st_name][ct_name],l, keys.CHILDREN_HOSPITAL)
        request = re.get(url)
        rescode = request.status_code

        if (rescode == 200):  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
            responseData = request.text
            rD = xtd.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
            rDJ = json.dumps(rD)  # dict 형식의 데이터를 json형식으로 변환
            rDD = json.loads(rDJ)  # json형식의 데이터를 dict 형식으로 변환

            w_data = rDD["response"]["body"]["items"]["item"]  # item에 포함된 data list
            total_count = int(rDD["response"]["body"]["totalCount"])  # 주어진 조건의 total count

            temp = []
            # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
            if total_count == 1:
                temp.append(w_data)
                w_data = temp

            for e in range(len(w_data)):
                print()
                print('검진기관 :', w_data[e]["orgnm"])
                print('주소 :', w_data[e]["orgAddr"])
                print('전화번호 :', w_data[e]["orgTlno"])
            print()

    return w_data
'''
print('='*10,'state','='*10)
stateSearch('제주특별자치도')
print('='*10,'city','='*10)
citySearch('서울','종로구')
'''