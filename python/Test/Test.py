# import json
# from humanfriendly import parse_date
# import requests
# #from datetime import date
# from datetime import datetime, timedelta

# today = datetime.now().date()
# yesterday = today - timedelta(days=1)
# yesterday_str = str(yesterday).replace('-', '')
# today_str = str(today).replace('-', '')
# print(yesterday_str)
# print(today_str)
# api = "https://apis.data.go.kr/1360000/BeachInfoservice/getVilageFcstBeach?serviceKey=DEF5XPkxhhq5F1Y2%2FwA8ZWYnFPEJ6UBjmVNTqzWg5KzBilcVtEtOslYXRSYWcDzM1iyrbKapwMAE0ucKHPhtQA%3D%3D&numOfRows=737&pageNo=10&dataType=JSON&base_date={}&base_time=1100&beach_num=1".format(yesterday_str)
# result = requests.get(api)
# result = json.loads(result.text)
# print(api)

# wav = []


# check = result['response']['body']['items']['item']
# #print(check)

# filtered_items = [item for item in check if (item['category'] == 'TMP' or item['category'] == 'WSD'
#                   or item['category'] == 'SKY' or item['category'] == 'PTY' or item['category'] == 'POP'
#                   or item['category'] == 'WAV'or item['category'] == 'PCP' or item['category'] == 'REH')  and datetime.strptime(item['fcstTime'], '%H%M') < datetime.strptime('1200', '%H%M') and item['fcstDate'] == '20230904']
# # check = filtered_items
# for i in filtered_items:
#     #wav.append(i['fcstValue'])
#     wav.append(i)

# print(wav)
# print(len(wav))
# # for i in check:
# #     print()
#     # for a in i:
#     #     print(a)
# # date_object = datetime.strptime("20230701", "%Y%m%d").date()
# # def compare_dates(target_date):
# #     today = datetime.today().date()
# #     print(today)
# #     print(target_date)
# #     if today > target_date:
# #         print("오늘은 정해진 날짜 이후입니다.")
# #     elif today < target_date:
# #         print("오늘은 정해진 날짜 이전입니다.")
# #     else:
# #         print("오늘은 정해진 날짜와 동일합니다.")
        
# # compare_dates(date_object)

import base64
import os
import DB.DB_TEST as DB

result = DB.View_Post()
encoded_image = base64.b64encode(result[0]).decode('utf-8')