'''전국 지역 코드를 dictionary 형태의 code.txt로 추출하는 python code'''
'''추출된 코드를 추가적으로 가공하였음, 따라서 이제 이 코드는 실행 하면 안됨!'''
from ast import literal_eval
import requests as re
import xmltodict as xtd
import json

# state code dictionary open
with open('state_code_children_hospital.txt','r',encoding='utf-8') as f:
    state = literal_eval(f.read())

code_dict = {}

# 시/구 별 코드 받아오는 메소드
def city_code(st_name):
  for i in range(len(state)):
    code_dict[st_name] = {}
    url = 'https://nip.cdc.go.kr/irapi/rest/getCondSggCd.do?brtcCd={0}&serviceKey=hZ6Exha7XAsIAyIinZz4Vycw8YtH9%2BVoNuCyaxhSW0UX3O8Zp5msTkN3UdHoiyR123LL2qKXHqZcF6WbM2PlJA%3D%3D'.format(state[st_name])
    request = re.get(url)
    rescode = request.status_code

    if(rescode == 200):
      responseData = request.text
        
      rD = xtd.parse(responseData)
      rDJ = json.dumps(rD)
      rDD = json.loads(rDJ)

      w_data = rDD["response"]["body"]["items"]["item"]
      total_count = int(rDD["response"]["body"]["totalCount"])
      temp = []

      # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
      if total_count == 1:
          temp.append(w_data)
          w_data = temp

      for e in range(len(w_data)):
          code = w_data[e]["cd"]
          name = w_data[e]["cdNm"]
          code_dict[st_name][name] = code

  # 시/구 별 코드를 저장
  with open('city_code_children_hospital.txt', 'w', encoding='utf-8') as f:
      f.write(str(code_dict))

# 실행 코드
# for key in state:
#     city_code(key)


      
