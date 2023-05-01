from dotenv import load_dotenv
import os
import requests
import json
from weather_crawling import crawl_and_store_message

with open("kakao_token.json","r") as json_file:
  tokens = json.load(json_file)

url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers={
"Authorization" : "Bearer " + tokens["access_token"]
}

data={ 
  "template_object": json.dumps({ 
      "object_type":"text", 
      "text": crawl_and_store_message(), 
      "link":{ 
        "web_url":"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%8C%80%ED%9D%A5+%EB%82%A0%EC%94%A8"

      }
    })
}
response = requests.post(url, headers=headers, data=data)
print(response.status_code)
if response.json().get('result_code') == 0:
  print('메시지를 성공적으로 보냈습니다!')
else:
  print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' +
str(response.json()))
info_url = "https://kapi.kakao.com/v2/user/scopes"
params = {"secure_resource": True}
info_res = requests.get(info_url, headers=headers, params=params)

print(info_res.json())