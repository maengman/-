from datetime import datetime, timedelta
import pymysql
import DB.Ocean as Ocean

timeck1 = datetime.now()
timeck2 = None


def Marine_Weather_Data():
    try:
        # 데이터베이스 연결
        con = pymysql.connect(host='localhost', user='root', password='1234', db='fishinglog', charset='utf8')
        cursor = con.cursor()

        # 해변 번호 범위 설정
        start_beach_number = 1
        end_beach_number = 420

        # 날짜 계산
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_str = str(yesterday).replace('-', '')
        today_str = str(today).replace('-', '')
         

        values_date = [today_str,] 
        values_time = []
        date = datetime.now().date()
        a=0
        for i in range(1, 73):
            if i % 24 == 0:
                date += timedelta(days=1)
            if(a==24):
                a=0
            if(a<10):
                values_time.append("0{}:00".format(a))
            elif(a>=10):
                values_time.append("{}:00".format(a))
            a+=1
            values_date.append(str(date).replace('-', ''))
        values_time.append("00:00")

    #데이터 입력
        batch_size = 8
        for beach_number in range(start_beach_number, end_beach_number + 1):
            weather = Ocean.OceanData(today_str, yesterday_str, beach_number)
            print(len(weather))
            values = []

            for i in range(0, len(weather), batch_size):
                batch_weather = tuple(weather[i:i + batch_size])
                test_value = values_date[i // batch_size]  # 해당 배치의 test 요소 선택 #나눈 몫을 나타내기
                test_value2 = values_time[i // batch_size]
                values.append((beach_number,) + batch_weather + (test_value,test_value2,))
    
            del values[-1]
            insert_weather_data(con, cursor, beach_number, values)
    
    except Exception as e:
        print(e)
        print("날씨 입력 실패")

    finally:
        cursor.close()
        con.close()
    timeck2 = datetime.now() 
    print(timeck1)
    print(timeck2)  



def insert_weather_data(con, cursor, beach_number, weather_data):
    try:
        sql = "INSERT INTO weatherinfo (beach_number, TMP, WSD, SKY, PTY, POP, WAV, PCP, REH, DATE, TIME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, weather_data)
        con.commit()
    except Exception as e:
        print(e)
        print(f"날씨 입력 실패 (해변 번호 {beach_number})")
        return beach_number
