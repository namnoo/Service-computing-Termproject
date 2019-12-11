#-*- coding:utf-8 -*-
import json
import xmltodict
import sys
import io
import requests as re

region = [1100000000,2600000000,2700000000,2800000000,2900000000,3000000000,3100000000,3600000000,4100000000,4200000000,4300000000,4400000000,4500000000,4600000000,4700000000,4800000000,5000000000
]

#maxpage=[119,35,27,33,19,19,12,5,147,13,16,18,18,14,24,33,8]

def search(keywords = None,location = 0):
  if location > 0 : cnt = 1
  else : cnt = len(region)
  for i in range(cnt):
    url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&searchWord={2}&serviceKey=hZ6Exha7XAsIAyIinZz4Vycw8YtH9%2BVoNuCyaxhSW0UX3O8Zp5msTkN3UdHoiyR123LL2qKXHqZcF6WbM2PlJA%3D%3D".format(region[i],1,keywords)

    request = re.get(url)

    rescode = request.status_code

    #제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
    if(rescode == 200):
      responseData = request.text

      #요청받은 데이터를 읽음
      rD = xmltodict.parse(responseData)
      #XML형식의 데이터를 dict형식으로 변환시켜줌

      rDJ = json.dumps(rD)
      #dict 형식의 데이터를 json형식으로 변환

      rDD = json.loads(rDJ)
      #json형식의 데이터를 dict 형식으로 변환

      maxPage = int(rDD["response"]["body"]["maxPage"])

    for j in range(1,maxPage+1):
      if location > 0 : url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&searchWord={2}&serviceKey=hZ6Exha7XAsIAyIinZz4Vycw8YtH9%2BVoNuCyaxhSW0UX3O8Zp5msTkN3UdHoiyR123LL2qKXHqZcF6WbM2PlJA%3D%3D".format(region[location-1],j,keywords)
      else : url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&searchTpcd=ADDR&searchWord={2}&serviceKey=hZ6Exha7XAsIAyIinZz4Vycw8YtH9%2BVoNuCyaxhSW0UX3O8Zp5msTkN3UdHoiyR123LL2qKXHqZcF6WbM2PlJA%3D%3D".format(region[i],j,keywords)
      #url = "https://nip.cdc.go.kr/irapi/rest/getOrgList.do?brtcCd={0}&pageNo={1}&numberOfRows=20&serviceKey=hZ6Exha7XAsIAyIinZz4Vycw8YtH9%2BVoNuCyaxhSW0UX3O8Zp5msTkN3UdHoiyR123LL2qKXHqZcF6WbM2PlJA%3D%3D".format(region[i],j)
      request = re.get(url)

      rescode = request.status_code

      #제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
      if(rescode == 200):
        responseData = request.text

        #요청받은 데이터를 읽음
        rD = xmltodict.parse(responseData)
        #XML형식의 데이터를 dict형식으로 변환시켜줌

        rDJ = json.dumps(rD)
        #dict 형식의 데이터를 json형식으로 변환

        rDD = json.loads(rDJ)
        #json형식의 데이터를 dict 형식으로 변환

        w_data = rDD["response"]["body"]["items"]["item"]
        temp = []
        if(len(w_data) == 4):
          temp.append(w_data)
          w_data = temp

        for e in range(len(w_data)):
          print()
          print('검진기관 :',w_data[e]["orgnm"])
          print('주소 :',w_data[e]["orgAddr"])
          print('전화번호 :',w_data[e]["orgTlno"])
        print()

if __name__ == "__main__":
  while(1):
    print("1. 전국검색 \n2. 시/도별 검색\n3. 나가기\n")
    option = int(input("원하는 검색 옵션을 선택하세요 : "))
    if option == 1:
      keywords = input("키워드를 입력하세요 : ")
      search(keywords)
    elif option == 2 :
      print("1. 서울  2. 부산 3. 대구 4. 인천 5. 광주 6. 대전 7. 울산 8. 세종 \n9. 경기도 10. 강원도 11. 충청북도 12. 충청남도 13. 전라북도 14. 전라남도 15. 경상북도 16. 경상남도 17. 제주특별자치도\n ")
      location = int(input("원하시는 시/도를 입력하세요 : "))
      keywords = input("키워드를 입력하세요 : ")
      search(keywords,location)
    else: break