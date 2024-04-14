# import os
# import requests
# import datetime
# import time

# class valid_api:
#     def __init__(self, count=10):
#         self.host = 'https://apis.data.go.kr/'
#         self.urls = [
#             '1360000/BeachInfoservice/getVilageFcstBeach?serviceKey=DEF5XPkxhhq5F1Y2%2FwA8ZWYnFPEJ6UBjmVNTqzWg5KzBilcVtEtOslYXRSYWcDzM1iyrbKapwMAE0ucKHPhtQA%3D%3D&numOfRows=737&pageNo=10&dataType=JSON&base_date=20230904&base_time=1100&beach_num=72'
#             ]
#         self.result = dict()
#         self.count = count

#     def validation(self):
#         for url in self.urls:
#             full_url = self.host + url
#             results = []
#             for i in range(self.count):
#                 start = datetime.datetime.now()
#                 res = requests.get(full_url)
#                 assert res.status_code == 200
#                 passed_t = datetime.datetime.now() - start
#                 results.append(passed_t.total_seconds())
#                 time.sleep(0.1)
#                 print(f'\rturn: {i + 1}', end='')
#             print()
#             print(url)
#             print(sum(results) / self.count)
#             self.result[url] = results

#     def save_results(self):
#         BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#         with open(os.path.join(BASE_DIR, f'{self.count}_api_validation.txt'), 'w') as f:
#             for k,v in self.result.items():
#                 doc = f"api: {k}\n"
#                 doc += f'mean: {sum(v) / len(v):.2f}\n'
#                 doc += f'max: {max(v):.2f}\n'
#                 doc += f'min: {min(v):.2f}\n\n'
#                 f.write(doc)

    

# if __name__ == '__main__':
#     tester = valid_api(100)
#     tester.validation()
#     tester.save_results()
from datetime import datetime, timedelta
import DB.Ocean as DB

today = datetime.now().date()
yesterday = today - timedelta(days=1)
yesterday_str = str(yesterday).replace('-', '')
today_str = str(today).replace('-', '')
test=[]
tt=datetime.now().date()
for i in range(1,585):
    if(i%24==0):
       tt += timedelta(days=1)
    test.append(str(tt).replace('-', ''))
testtuu = tuple(test)
print(test)