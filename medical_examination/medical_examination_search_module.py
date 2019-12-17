import json
from ast import literal_eval
import requests as re
import xmltodict as xtd
import keys

# 시/도 단위 코드 read
with open('medical_examination/state_code_medical_examination.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

# 시/구 단위 코드 read
with open('medical_examination/city_code_medical_examination.txt','r',encoding='utf-8') as f:
    city = literal_eval(f.read())

# 건강검진 항목 딕셔너리
examination_dict={'grenChrgTypeCd':'일반검진','ichkChrgTypeCd':'영유아검진','bcExmdChrgTypeCd':'유방암','ccExmdChrgTypeCd':'대장암','cvxcaExmdChrgTypeCd':'자궁경부암','lvcaExmdChrgTypeCd':'간암','mchkChrgTypeCd':'구강','stmcaExmdChrgTypeCd':'위암'}

# 시/도 단위 검색(사용안함)
def stateSearch(st_name):
    state_list = []

    url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?siDoCd={0}&ServiceKey={1}".format(state[st_name],
        keys.MEDICAL_EXAMINATION)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):
        responseData = request.text
        rD = xtd.parse(responseData)
        rDJ = json.dumps(rD)
        rDD = json.loads(rDJ)

        totalCount = int(rDD["response"]["body"]["totalCount"])
        maxPage = (totalCount // 10) + 1 #maxPage가 존재하지 않아서 totalCount // 10 + 1로 저장

        for l in range(1,maxPage):
         url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?pageNo={0}&siDoCd={1}&ServiceKey={2}".format(l,state[st_name],keys.MEDICAL_EXAMINATION)
         request = re.get(url)
         rescode = request.status_code

         if (rescode == 200):
            responseData = request.text
            rD = xtd.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

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
                if "hmcTelNo" in w_data[e]: # 전화번호가 존재하지 않는 경우 None 처리
                    state_list.append({"orgnm": w_data[e]["hmcNm"],
                                       "orgEmn": examination,
                                       "orgTlno": w_data[e]["hmcTelNo"],
                                       "orgAddr": w_data[e]["locAddr"]})
                else:
                    state_list.append({"orgnm": w_data[e]["hmcNm"],
                                       "orgEmn": examination,
                                       "orgTlno": None,
                                       "orgAddr": w_data[e]["locAddr"]})

            state_dict = {"result":
                              {"type": '검진기관',
                               "list": state_list}
                          }
    return state_dict

# 시/구 단위 검색
def citySearch(st_name,ct_name):
    city_list = []

    url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?siDoCd={0}&siGunGuCd={1}&ServiceKey={2}".format(state[st_name],city[st_name][ct_name],keys.MEDICAL_EXAMINATION)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):
        responseData = request.text
        rD = xtd.parse(responseData)
        rDJ = json.dumps(rD)
        rDD = json.loads(rDJ)

        totalCount = int(rDD["response"]["body"]["totalCount"])
        maxPage = (totalCount // 10) + 1

        for l in range(1,maxPage):
         url = "http://openapi1.nhis.or.kr/openapi/service/rest/HmcSearchService/getHmcList?pageNo={0}&siDoCd={1}&siGunGuCd={2}&ServiceKey={3}".format(l,state[st_name],city[st_name][ct_name],keys.MEDICAL_EXAMINATION)
         request = re.get(url)
         rescode = request.status_code

         if (rescode == 200):
            responseData = request.text
            rD = xtd.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

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
                if "hmcTelNo" in w_data[e]: # 전화번호가 존재하지 않는 경우 None
                    city_list.append({"orgnm": w_data[e]["hmcNm"],
                                      "orgEmn": examination,
                                      "orgTlno": w_data[e]["hmcTelNo"],
                                      "orgAddr": w_data[e]["locAddr"]})
                else:
                    city_list.append({"orgnm": w_data[e]["hmcNm"],
                                      "orgEmn": examination,
                                      "orgTlno": None,
                                      "orgAddr": w_data[e]["locAddr"]})

            city_dict = {"result":
                             {"type": '검진기관',
                              "list": city_list}
                         }

            dictToJson = json.dumps(city_dict, ensure_ascii=False)

    return dictToJson

# 전국 검색(사용안함)
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

# result = citySearch('인천시','계양구')
# pprint.pprint(result)

