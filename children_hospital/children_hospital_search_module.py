import requests as re
import xmltodict as xtd
import keys
import json
from ast import literal_eval

# 시/도 코드 딕셔너리 read
with open('children_hospital/state_code_children_hospital.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

# 시/구 딕셔너리 read
with open('children_hospital/city_code_children_hospital.txt','r',encoding='utf-8') as f:
    city = literal_eval(f.read())


# 시/도 별 검색(사용안함)
def stateSearch(st_name):
    state_list = []

    url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&serviceKey={2}".format(state[st_name],1,keys.CHILDREN_HOSPITAL)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200): # 데이터 수신 성공시
        responseData = request.text
        rD = xtd.parse(responseData)
        rDJ = json.dumps(rD)
        rDD = json.loads(rDJ)

        maxPage = int(rDD["response"]["body"]["maxPage"]) # 최대 페이지 수를 저장

    for l in range(1,maxPage+1): # 최대 페이지까지 반복해서 참조
        url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&serviceKey={2}".format(
            state[st_name], l, keys.CHILDREN_HOSPITAL)
        request = re.get(url)
        rescode = request.status_code

        if (rescode == 200): # 올바른 응답 발생시 수행
            responseData = request.text
            rD = xtd.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)

            w_data = rDD["response"]["body"]["items"]["item"] # xml의 item 참조
            total_count = int(rDD["response"]["body"]["totalCount"]) # item의 전체 갯수
            temp = []

            # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
            if total_count == 1:
                temp.append(w_data)
                w_data = temp

            # 조건을 만족하는 모든 데이터를 dictionary 형식으로 리스트에 추가
            for e in range(len(w_data)):
                state_list.append({"c_orgnm": w_data[e]["orgnm"],
                                   "c_orgAddr": w_data[e]["orgAddr"],
                                   "c_orgTlno": w_data[e]["orgTlno"]})
            state_dict = {"result":
                             {"type": '어린이 예방접종기관',
                              "list": state_list}
                         }

    return state_dict

index = 0 # return 값 index를 출력하기 위한 index 변수
# 시/구 별 검색
def citySearch(st_name,ct_name):

    global index
    city_list = []
    exceptlist = ['전주시 완산구', '전주시 덕진구', '창원시 성산구', '창원시 의창구', '창원시 마산회원구', '창원시 마산합포구'] # 검색 예외 처리 리스트

    url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&sggCd={1}&pageNo={2}&numberOfRows=20&searchTpcd=ADDR&serviceKey={3}".format(
        state[st_name], city[st_name][ct_name], 1, keys.CHILDREN_HOSPITAL)
    request = re.get(url)
    rescode = request.status_code

    if (rescode == 200):  # 올바른 응답 발생시 수행
        responseData = request.text
        rD = xtd.parse(responseData)
        rDJ = json.dumps(rD)
        rDD = json.loads(rDJ)
        check = int(rDD["response"]["header"]["resultCode"]) # 200이 응답되어도 limited 에러가 자주 발생하여 resultCode check
        maxPage = int(rDD["response"]["body"]["maxPage"]) # 최대 페이지 수 저장

        if (check == 22): # 만약 check된 resultCode가 22라면, url의 내용을 다시 로드함
            while check == 22: # resultCode가 00이 될때까지 while 루프 실행
                request = re.get(url)
                responseData = request.text
                rD = xtd.parse(responseData)
                rDJ = json.dumps(rD)
                rDD = json.loads(rDJ)
                check = int(rDD["response"]["header"]["resultCode"]) # 루프가 실행될 때마다 check값을 update
                maxPage = int(rDD["response"]["body"]["maxPage"]) # 루프가 실행될 때마다 maxPage값을 update

    for l in range(1, maxPage+1): # 최대 페이지까지 반복해서 참조
        url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&sggCd={1}&pageNo={2}&numberOfRows=20&searchTpcd=ADDR&serviceKey={3}".format(
            state[st_name],city[st_name][ct_name],l, keys.CHILDREN_HOSPITAL)
        request = re.get(url)
        rescode = request.status_code
        # print(url)
        if (rescode == 200):
            responseData = request.text
            rD = xtd.parse(responseData)
            rDJ = json.dumps(rD)
            rDD = json.loads(rDJ)
            w_temp = rDD["response"]["body"]["items"] # xml의 items 참조
            total_count = int(rDD["response"]["body"]["totalCount"]) # item의 전체 갯수

            if w_temp == None: # 만약에 참조된 items가 None이면
                while w_temp == None: # items가 None이 아닌 값이 될 때까지 while 루프 실행
                    request = re.get(url) # url값에서 내용을 제대로 받아오지 못하는 에러이므로 값을 다시 받아옴
                    responseData = request.text
                    rD = xtd.parse(responseData)
                    rDJ = json.dumps(rD)
                    rDD = json.loads(rDJ)
                    w_temp = rDD["response"]["body"]["items"] # 루프가 실행될 때 마다 w_temp값을 update
                    total_count = int(rDD["response"]["body"]["totalCount"]) # 루프가 실행될 때마다 total_count값을 update

            w_data = w_temp["item"]
            temp = []
            # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
            if total_count == 1:
                temp.append(w_data)
                w_data = temp

            for e in range(len(w_data)):
                if ct_name in exceptlist: # 시/구 코드가 겹칠경우에
                    for i in range(len(exceptlist)):
                        if ct_name == exceptlist[i]: # 코드값 + 주소 키워드를 사용하여 결과값을 반환
                            if w_data[e]["orgAddr"].find(exceptlist[i]) != -1:
                                city_list.append({"c_orgnm": w_data[e]["orgnm"],
                                                  "c_orgAddr": w_data[e]["orgAddr"],
                                                  "c_orgTlno": w_data[e]["orgTlno"]})
                            else: break

                else:
                    city_list.append({"c_orgnm": w_data[e]["orgnm"],
                                      "c_orgAddr": w_data[e]["orgAddr"],
                                      "c_orgTlno": w_data[e]["orgTlno"]})

            city_dict = {"result":
                             {"type": '어린이 예방접종기관',
                              "list": city_list}
                         }

            dictToJson = json.dumps(city_dict, ensure_ascii=False)

    return dictToJson

def searchAll(): # 전국 검색(사용안함)
    key = []
    for s in state.keys():
        key.append(s)
    for k in key:
        result = stateSearch(str(k))
        return result
