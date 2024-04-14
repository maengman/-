# import base64
# import gzip
# import json
# import os

# from flask import jsonify
# import DB.DB_TEST as DB

# # result = DB.View_Post()
# # # json_data = json.dumps(result)
# # # json_bytes = json_data.encode('utf-8')
# # # compressed_data = gzip.compress(json_bytes)
# # # encoded_image = base64.b64encode(compressed_data).decode('utf-8')
# # # response = {'result': encoded_image}
# # # print(response) 


# result = DB.View_Post()
# json_data = json.dumps(result)
# json_bytes = json_data.encode('utf-8')
# compressed_data = gzip.compress(json_bytes)
# response = {'result': compressed_data}
# print(response)
# # print(jsonify(response))


# from flask import Flask, request, jsonify
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'  # 이미지를 저장할 디렉토리 설정

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'image' in request.files:
#         image = request.files['image']
#         if image:
#             filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
#             image.save(filename)

#             # 이미지 URL 생성
#             image_url = f'http://yourserver.com/{filename}'

#             return jsonify({'image_url': image_url}), 200
#         else:
#             return 'Invalid image', 400
#     else:
#         return 'Image not found', 400

# if __name__ == '__main__':
#     app.run()



# # coding: utf-8
# import base64
# import requests
# import json

# openApiURL = "https://2maargjyfo.apigw.ntruss.com/fishlens/v1/predict"
# accessKey = "loo6kTk4fhCZlTsOViFdChUtzyOmtbawdpl7gA4J"
# imageFilePath = r"C:\Users\MM\Desktop\ffe834b9-39f0-48ef-803b-79660cb10daf.jpg"

# # multipart/form-data
# file = {'file': open(imageFilePath, 'rb')}

# headers = {
# "x-ncp-apigw-api-key": accessKey
# }

# response = requests.post(openApiURL, headers=headers, files=file)
# # 응답 확인
# data = json.loads(response.text)
# print("[responseCode] " + str(response.status_code))
# print("[responseBody]")
# print(data['detail'])

# if 'image' in data and data['image'] is not None:
#     with open("responsedImg.png", "wb") as fh:
#         fh.write(base64.b64decode(data['image']))
#     print('Image Saved')



# import os
# import sys
# import urllib.request
# client_id = "rrMCMPlEU5Kit5D7YMP2"
# client_secret = "opYIEq6XGE"
# encText = urllib.parse.quote("상실의 시대")
# url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
# # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if(rescode==200):
#     response_body = response.read()
#     print(response_body.decode('utf-8'))
# else:
#     print("Error Code:" + rescode)
    
    
import os
import sys
import urllib.request
client_id = "rrMCMPlEU5Kit5D7YMP2"
client_secret = "opYIEq6XGE"
url = "https://openapi.naver.com/v1/datalab/shopping/categories";
body = "{\"startDate\":\"2023-10-01\",\"endDate\":\"2023-11-13\",\"timeUnit\":\"month\",\"category\":[{\"name\":\"무라카미 하루키\",\"param\":[\"50000000\"]},{\"name\":\"상실의시대\",\"param\":[\"50000002\"]}],\"device\":\"pc\",\"ages\":[\"20\",\"30\"],\"gender\":\"f\"}";

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)