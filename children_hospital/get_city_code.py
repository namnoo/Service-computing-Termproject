#-*- coding:utf-8 -*-
'''전국 지역 코드를 dictionary 형태의 code.txt로 추출하는 python code'''

import requests as re
import xmltodict as xtd
import json
import sys
import io

region = [1100000000,2600000000,2700000000,2800000000,2900000000,3000000000,3100000000,3600000000,4100000000,
          4200000000,4300000000,4400000000,4500000000,4600000000,4700000000,4800000000,5000000000] 

code_dict = {}

#def children_hospital(keywords = None, location = 0):
def children_hospital():
  for i in range(len(region)):
    url = 'https://nip.cdc.go.kr/irapi/rest/getCondSggCd.do?brtcCd={0}&serviceKey=hZ6Exha7XAsIAyIinZz4Vycw8YtH9%2BVoNuCyaxhSW0UX3O8Zp5msTkN3UdHoiyR123LL2qKXHqZcF6WbM2PlJA%3D%3D'.format(region[i])
    request = re.get(url)
    rescode = request.status_code

    if(rescode == 200):
      responseData = request.text
        
      rD = xtd.parse(responseData)
      rDJ = json.dumps(rD)
      rDD = json.loads(rDJ)

      w_data = rDD["response"]["body"]["items"]["item"] #item에 포함된 data list
      total_count = int(rDD["response"]["body"]["totalCount"]) #주어진 조건의 total count
      temp = []
      # total count가 1일 경우 dictionary를 원소로 가지는 list가 생성 되지 않는 예외 처리
      if total_count == 1:
          temp.append(w_data)
          w_data = temp

      for e in range(len(w_data)):
          code = w_data[e]["cd"]
          name = w_data[e]["cdNm"]
          code_dict[name] = code
          
children_hospital()

with open('code.txt','w',encoding='utf-8') as f:
    f.write(str(code_dict))
    print("open")
      
