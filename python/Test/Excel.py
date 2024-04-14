import pandas as pd
import pymysql

# MySQL DB 연결 정보 설정

# Excel 파일 경로
excel_file = r"C:\Users\MM\Desktop\코딩관련\바다낚시 팁.xlsx"

# Excel 파일에서 데이터 읽기
df = pd.read_excel(excel_file,)

# MySQL DB에 연결
con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8')
cursor = con.cursor()

# 데이터 삽입 쿼리
insert_query = '''
INSERT INTO fishinglog.fishing_tip (post_link, post_name, post_maker, post_type) VALUES (%s, %s, %s, %s)
'''
test=[]

# 데이터 삽입
for _, row in df.iterrows():
    post_link = row['링크']
    post_name = row['제목']
    post_maker = row['작성자']
    post_type = row['유형']
    values = (post_link, post_name, post_maker, post_type)
    cursor.execute(insert_query, values)
con.commit()
print("입력완료")
con.close()



# import pandas as pd
# import pymysql

# # MySQL DB 연결 정보 설정

# # Excel 파일 경로
# excel_file = r"C:\Users\MM\Desktop\코딩관련\어종 금어기 정리본.xlsx"

# # Excel 파일에서 데이터 읽기
# df = pd.read_excel(excel_file)

# # NaN 값을 None으로 변경 (NaT 포함)
# #df = df.where(pd.notna(df), 2023-00-00)
# #df.fillna(value=2023-01, inplace=True)

# # df = df.replace({pd.NaT : None}, inplace=True)
# print(df)

# # MySQL DB에 연결
# con = pymysql.connect(host='localhost', user='root', password='1234',
#                        db='fishinglog', charset='utf8')
# cursor = con.cursor()

# # 데이터 삽입 쿼리
# insert_query = '''
# INSERT INTO fishinglog.banned (fish_image, fish_name, ban_date, ban_cm, from_fish_image, ban_date_start, ban_date_end)
# VALUES (%s, %s, %s, %s, %s, %s, %s)
# '''

# # 데이터 삽입
# for _, row in df.iterrows():
#     fish_image = row['이미지']
#     fish_name = row['이름']
#     ban_date = row['금어기']
#     ban_cm = row['금지체장']
#     from_fish_image = row['이미지출처']
#     ban_date_start = row['금어기시작']
#     # if ban_date_start is None:  # 'NaT' 값이 아닐 경우에만 MySQL에 저장
#     #     ban_date_start = "asdafafsafsafsaf"  # 날짜 형식으로 변환
#     ban_date_end = row['금어기끝']
#     # if ban_date_end is None:  # 'NaT' 값이 아닐 경우에만 MySQL에 저장
#     #     ban_date_end = "asdafafsafsafsaf"  # 날짜 형식으로 변환
#     values = (fish_image, fish_name, ban_date, ban_cm, from_fish_image, ban_date_start, ban_date_end)
#     print(values)
#     cursor.execute(insert_query, values)

# # 변경사항 저장 및 연결 종료
# con.commit()
# con.close()




# # 데이터 삽입 쿼리
# insert_query = '''
# INSERT INTO fishwiki (fish_image, fish_name, danger, danger_point, season, recommend, look, fish_image_from, banded) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
# '''
# test=[]

# # 데이터 삽입
# for _, row in df.iterrows():
#     fish_image = row['이미지']
#     fish_name = row['이름']
#     danger = row['위험도']
#     danger_point = row['위험부위']
#     season = row['제철']
#     recommend = row['추천요리']
#     look = row['생김새']
#     fish_image_from = row['이미지 출처']
#     banded = row['금어기 및 금지체장']
#     values = (fish_image, fish_name, danger, danger_point, season, recommend, look, fish_image_from, banded)
#     cursor.execute(insert_query, values)

# 데이터 삽입
# for _, row in df.iterrows():
#     beach_name = row['해수욕장']
#     beach_number = row['순번']
#     lat = row['위도']
#     lon = row['경도']
#     values = (beach_name, beach_number, lat, lon)
#     cursor.execute(insert_query, values)
    
    

# for _, row in df.iterrows():
#     beach_name = row['해수욕장']
#     beach_number = row['순번']
#     lat = row['위도']
#     lon = row['경도']
#     where = row['지역']
#     values = (beach_name, beach_number, lat, lon)
#     File = open("C:\\Users\\MM\\Desktop\\MarineData", "a")
#     File.write(("'"+beach_name+"'"+" ,"))
#     File.write("\n")
#     File.close()
#     #cursor.execute(insert_query, values)



# where2 = "경남"
# for _, row in df.iterrows():
#     beach_name = row['해수욕장']
#     where = row['지역']
#     File = open("C:\\Users\\MM\\Desktop\\MarineData.txt", "a")
#     if(where == where2):
#         File.write(("'"+beach_name+"'"+" ,"))
#         File.write("\n")
#         File.close()
#     #cursor.execute(insert_query, values)
# File = open("C:\\Users\\MM\\Desktop\\MarineData.txt", "a")
# File.write(("--------------------"+where2+"\n"))
# File.close()


# # 커밋
# con.commit()
# print("끝")
# # 연결 종료
# cursor.close()
# con.close()
