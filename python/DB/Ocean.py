import json
import requests
from datetime import datetime, timedelta



def YesterDayOceanWeather(yesterDay,today,beach_number):
   
    WeatherData=[]
    api = "https://apihub.kma.go.kr/api/typ02/openApi/BeachInfoservice/getVilageFcstBeach?numOfRows=737&pageNo=2&dataType=JSON&base_date={}&base_time=1100&beach_num=150&authKey=PtNT74EsSDqTU--BLNg6fQ".format(yesterDay)
    api0 = "https://apis.data.go.kr/1360000/BeachInfoservice/getVilageFcstBeach?serviceKey=DEF5XPkxhhq5F1Y2%2FwA8ZWYnFPEJ6UBjmVNTqzWg5KzBilcVtEtOslYXRSYWcDzM1iyrbKapwMAE0ucKHPhtQA%3D%3D&numOfRows=737&pageNo=10&dataType=JSON&base_date={}&base_time=1100&beach_num={}".format(yesterDay,beach_number)
    print(api0)
    try:
        result = requests.get(api0)
        result = json.loads(result.text)
     
        yesterDayData = result['response']['body']['items']['item']
        filtered_items = [item for item in yesterDayData if (item['category'] == 'TMP' or item['category'] == 'WSD'
                    or item['category'] == 'SKY' or item['category'] == 'PTY' or item['category'] == 'POP'
                    or item['category'] == 'WAV' or item['category'] == 'PCP' or item['category'] == 'REH')  and datetime.strptime(item['fcstTime'], '%H%M') < datetime.strptime('1200', '%H%M') and item['fcstDate'] == today]

        for i in filtered_items:
            WeatherData.append(i['fcstValue'])
        return WeatherData

    except Exception as e:
        print("어제 오류 : ")
        print("-------------------------------------------------------")
        return False
    # print(WeatherData)
    
def TodayOceanWeather(today,beach_number):
    WeatherData=[]
    api = "https://apihub.kma.go.kr/api/typ02/openApi/BeachInfoservice/getVilageFcstBeach?numOfRows=737&pageNo=2&dataType=JSON&base_date={}&base_time=1100&beach_num=150&authKey=PtNT74EsSDqTU--BLNg6fQ".format(today)
    api0 = "https://apis.data.go.kr/1360000/BeachInfoservice/getVilageFcstBeach?serviceKey=DEF5XPkxhhq5F1Y2%2FwA8ZWYnFPEJ6UBjmVNTqzWg5KzBilcVtEtOslYXRSYWcDzM1iyrbKapwMAE0ucKHPhtQA%3D%3D&numOfRows=737&pageNo=10&dataType=JSON&base_date={}&base_time=1100&beach_num={}".format(today,beach_number)

    print(api0)
    try:
        result = requests.get(api0)
        result = json.loads(result.text)

        yesterDayData = result['response']['body']['items']['item']
        filtered_items = [item for item in yesterDayData if (item['category'] == 'TMP' or item['category'] == 'WSD'
                    or item['category'] == 'SKY' or item['category'] == 'PTY' or item['category'] == 'POP'
                    or item['category'] == 'WAV' or item['category'] == 'PCP' or item['category'] == 'REH')]

        for i in filtered_items:
            WeatherData.append(i['fcstValue'])
        #print(WeatherData)
        return WeatherData
    except Exception as e:
        print("오늘 오류 : ")
        print("-------------------------------------------------------")
        print(e)
        return False
        
 
def OceanData(today, yesterDay,beach_number):
    # print(today)
    # print(yesterDay)
    yesterDayWeather = YesterDayOceanWeather(yesterDay, today, beach_number)
    if(yesterDayWeather == False):
        print("어제 오류 메인 ")
        while True:
            if (YesterDayOceanWeather(yesterDay, today, beach_number)) != False:
                yesterDayWeather = YesterDayOceanWeather(yesterDay, today, beach_number)
                break
    todayWeather = TodayOceanWeather(today, beach_number)
    if (todayWeather == False):
        print("오늘 오류 메인 ")
        while True:
            if(TodayOceanWeather(today, beach_number) != False):
                todayWeather = TodayOceanWeather(today, beach_number)
                break 
    WeatherData = yesterDayWeather + todayWeather  # 두 리스트 합치기
    WeatherData2 = WeatherData
    WeatherData=[]
    #print(WeatherData)
    return WeatherData2
    