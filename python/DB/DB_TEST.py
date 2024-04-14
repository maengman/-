
import base64
import gzip
import os
import pymysql

def Select_Profile(user_nick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        # 커서 생성
        # 예시: 특정 조건에 맞는 행의 내용 수정
        update_sql = "SELECT user_profile FROM fishinglog.usertable WHERE userNick = %s;"
        cur = con.cursor()  
        cur.execute(update_sql, (user_nick))
        result = cur.fetchone()[0]
        
        return result
    finally:
        # 연결 종료
        con.close()

def upload_Pfrofile(image_path,user_nick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        # 커서 생성
        # 예시: 특정 조건에 맞는 행의 내용 수정
        update_sql = "UPDATE fishinglog.usertable SET user_profile = %s WHERE userNick = %s;"
        cur = con.cursor()  
        cur.execute(update_sql, (image_path , user_nick))
        # 변경사항 커밋
        con.commit()

    finally:
        # 연결 종료
        con.close()
   

def like_load(user_nick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        save_data_sql = "SELECT post_id FROM fishinglog.post_like WHERE user_nick = (%s);"
        cur = con.cursor()  
        cur.execute(save_data_sql, (user_nick))
        result = cur.fetchall()
        return_data = []
        for i in range(0, len(result)):

            return_data.append(str(result[i][0]))

        return return_data
    except Exception as e:
        print(e)
        return "다시 한번 해주십시오"
    finally:
        con.close()

def update_like(post_id,type,user_nick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        if(type == "like"):
            like_sql = "UPDATE fishinglog.post SET post_like = post_like + 1 WHERE post_id = (%s);"
            cur = con.cursor()  
            cur.execute(like_sql, (post_id))
            con.commit()
            sql_insert = "INSERT INTO fishinglog.post_like(post_id, user_nick) VALUES (%s, %s)"
            cur = con.cursor()  
            cur.execute(sql_insert, (post_id, user_nick))
        #cur.execute("SELECT LAST_INSERT_ID()")
        #ost_id = cur.fetchone()[0]
        #print("Inserted post_id:", post_id) 
            
        #cur.execute("SELECT LAST_INSERT_ID()")
        #ost_id = cur.fetchone()[0]
        #print("Inserted post_id:", post_id) 
            con.commit()
            return "좋아요"
        elif(type == "un_like"):
            un_like_sql = "UPDATE fishinglog.post SET post_like = post_like - 1 WHERE post_id = (%s);"
            cur = con.cursor()  
            cur.execute(un_like_sql, (post_id))
            con.commit()
            sql_delete = "delete FROM fishinglog.post_like where post_id = (%s) and user_nick = (%s)"
            cur = con.cursor()  
            cur.execute(sql_delete, (post_id, user_nick))
            con.commit()
            return "좋아요 취소"
    except Exception as e:
        print(e)
        return "다시 한번 해주십시오"
    finally:
        con.close()

def select_post_comment(post_id):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        sql = "select user_nick,user_comment from fishinglog.post_comment where post_id = (%s)"
        cur = con.cursor()  
        cur.execute(sql, (post_id))
        result = list(cur.fetchall())
        # for i in range(0, len(result)):
        #     print(result[i])
        return result
    except Exception as e:
        print(e)
        return "다시 한번 해주십시오"
    finally:
        con.close()

def user_post_comment(user_comment, post_id, user_nick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        sql = "INSERT INTO fishinglog.post_comment(user_comment, post_id, user_nick) VALUES ( %s, %s, %s)"
        cur = con.cursor()  
        cur.execute(sql, (user_comment, post_id, user_nick))
        #cur.execute("SELECT LAST_INSERT_ID()")
        #ost_id = cur.fetchone()[0]
        #print("Inserted post_id:", post_id) 
        con.commit()
        return "댓글 성공"
    except Exception as e:
        print(e)
        return "다시 한번 해주십시오"
    finally:
        con.close()

def delete_post(post_id):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "delete FROM fishinglog.post where post_id = %s;"
        cur = con.cursor()  
        cur.execute(sql, (post_id,))
        result = "삭제 되었습니다."
        return result
    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"
    finally:
        con.commit()
        con.close()
        
def My_Post_Like(user_id):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT * from fishinglog.post_like where user_nick = (%s) ORDER BY post_id DESC"
        cur.execute(sql, (user_id,))
        result = cur.fetchall()
        result_data = []
        for i in range(0,len(result)):
            data = list(result[i])
            sql2 = "SELECT fishinglog.post.post_id,fishinglog.post.user_date,fishinglog.post.user_text,fishinglog.post.user_id, post_like,GROUP_CONCAT(fishinglog.post_image.image_name) AS image_names FROM fishinglog.post LEFT JOIN  fishinglog.post_image ON fishinglog.post.post_id = fishinglog.post_image.post_id WHERE fishinglog.post.post_id = %s GROUP BY fishinglog.post.post_id ORDER BY post_id DESC;"
            cur.execute(sql2, (data[1],))
            data.append(list(cur.fetchall()))
            sql3 = "SELECT COUNT(*) FROM fishinglog.post_comment where post_id = %s"
            cur.execute(sql3,(str(data[1])))
            result_comment = cur.fetchone()[0]
            #print(sql3,(str(data[1])))
            data.append(str(result_comment))
            result_data.append(data)
        return result_data
       

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()

def MyPage(user_id):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT fishinglog.post.post_id,fishinglog.post.user_date,fishinglog.post.user_text,fishinglog.post.user_id, post_like,GROUP_CONCAT(fishinglog.post_image.image_name) AS image_names FROM fishinglog.post LEFT JOIN  fishinglog.post_image ON fishinglog.post.post_id = fishinglog.post_image.post_id WHERE fishinglog.post.user_id = %s GROUP BY fishinglog.post.post_id ORDER BY post_id DESC;"
        cur.execute(sql, (user_id,))
        result = cur.fetchall()
        result_data = []
        for i in range(0, len(result)):
           data = list(result[i])
           sql2 = "SELECT COUNT(*) FROM fishinglog.post_comment where post_id = %s"
           cur.execute(sql2,(str(data[i])))
           result_comment = cur.fetchone()[0]
           data.append(str(result_comment))
           result_data.append(data)
        return result_data
    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"
    finally:
        con.close()

def Search_Fishing_Tip():
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT * FROM fishinglog.fishing_tip"

        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()

def Search_Now_banned_fish():
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT * FROM fishinglog.banned WHERE CURDATE() BETWEEN ban_date_start AND ban_date_end"

        cur.execute(sql)
        result_post = cur.fetchall()
        return result_post

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()
        
def Search_CM_banned_fish():
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT * FROM fishinglog.banned where ban_cm != %s"

        cur.execute(sql,"X")
        result_post = cur.fetchall()
        return result_post

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()

def SelectFishWiki(fishname):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT * FROM fishinglog.fishwiki WHERE fish_name=%s"
        cur.execute(sql, fishname)
        result_post = cur.fetchone()
        return result_post

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()

def Fish_Ban():
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT * FROM fishinglog.banned"
        cur.execute(sql,)
        result_post = cur.fetchall()
        return result_post

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()        


def View_Post_Image(post_id):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:

        sql_image = "SELECT image_name FROM fishinglog.post_image where post_id = {}".format(post_id)
        cur = con.cursor()
        cur.execute(sql_image)
        result_post = cur.fetchall()
        
        return list(result_post)
    
    except Exception as e:
        print(e)
        return "다시 한번 해주세요"

    finally:
        con.close() 
        
         
def View_Post_POST(post_id):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        sql = "SELECT * FROM fishinglog.post where post_id = (%s)"
        cur = con.cursor()
        cur.execute(sql,(post_id))
        result_post = cur.fetchall()
        
        test = []
        for i in range(0, len(result_post)):

            a = list(result_post[i])
            post_image = View_Post_Image(a[0])
            for c in range(0, len(post_image)):
                #encoded_image = base64.b64encode(post_image[c][0]).decode('utf-8')
                a.append(post_image[c][0])
            sql2 = "SELECT COUNT(*) FROM fishinglog.post_comment where post_id = %s"
            cur.execute(sql2,(str(a[0])))
            # print(str(a[0]))
            result_comment = cur.fetchone()[0]
            a.append(str(result_comment))
            test.append(a)
            # result[i].append("asdf")
        return test

    except Exception as e:
        print(e)
        return "다시 한번 해주세요"

    finally:
        con.close()  



def View_Post_GET():
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        sql = "SELECT * FROM fishinglog.post ORDER BY post_id DESC LIMIT 10;"
        cur = con.cursor()
        cur.execute(sql)
        result_post = cur.fetchall()
        
        test = []
        for i in range(0, len(result_post)):
            a = list(result_post[i])
            post_image = View_Post_Image(a[0])
            for c in range(0, len(post_image)):
                a.append(post_image[c][0])
            sql2 = "SELECT COUNT(*) FROM fishinglog.post_comment where post_id = %s"
            cur.execute(sql2,(str(a[0])))
            result_comment = cur.fetchone()[0]
            a.append(str(result_comment))
            test.append(a)
        return test

    except Exception as e:
        print(e)
        return "다시 한번 해주세요"

    finally:
        con.close()  


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData



def user_post(lat, lon, user_date, user_text, user_id, user_Location):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        sql = "INSERT INTO fishinglog.post(lat, lon, user_date, user_text, user_id, user_Location) VALUES ( %s, %s, %s, %s, %s, %s)"
        cur = con.cursor()  
        cur.execute(sql, (lat, lon, user_date, user_text, user_id, user_Location))
        cur.execute("SELECT LAST_INSERT_ID()")
        post_id = cur.fetchone()[0]
        con.commit()
        return post_id
    except Exception as e:
        print(e)
    finally:
        con.close()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def user_post_image(image, post_id, image_name):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        data = convertToBinaryData(image)
        
        sql = "INSERT INTO fishinglog.post_image(image, post_id, image_name) VALUES (%s, %s, %s)"
        cur = con.cursor()  
        cur.execute(sql, (data, post_id, image_name))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        con.close()


def Marine_Weather(beachname):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        sql = "SELECT beach_number FROM fishinglog.beachinfo WHERE beach_name=%s"
        cur.execute(sql, beachname)
        beach_number= cur.fetchone()
        sql = "SELECT * FROM fishinglog.weatherinfo WHERE beach_number=%s"
        cur.execute(sql, beach_number[0])
        result = cur.fetchall()
        modified_result = [row[2:] for row in result]
        return modified_result

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()


def UserSignup(userID, userPW, userNick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:  
        
        if(CkeckUserID(userID) == "FALSE"):
            return "아이디가 중복입니다"      
        
        if(CkeckUserNick(userNick) == "FALSE"):
            return "닉네임이 중복입니다" 
        sql = "INSERT INTO usertable(userID, userPW, userNick) VALUES (%s, %s, %s)"
        cur = con.cursor()  
        cur.execute(sql, (userID, userPW, userNick))
        con.commit()
        return "회원가입 되었습니다"
    except Exception as e:
        print(e)
        return "다시 한번 해주세요"
        
# STEP 5: DB 연결 종료
    finally:
        con.close() 
        
def CkeckUserID(userID):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT userID FROM fishinglog.usertable WHERE userID=%s"
        cur.execute(sql, userID)
        
        if cur.rowcount > 0:
            # 이미 존재하는 경우
            return "FALSE"
        else:
            # 존재하지 않는 경우
            return "TRUE"

    except Exception as e:
        print(e)
        print("dberror")
        return "다시 한번 해주십시오"

    finally:
        con.close()
        
        
def CkeckUserNick(userNick):
    con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        cur = con.cursor()
        # 아이디나 닉네임이 이미 데이터베이스에 존재하는지 확인
        sql = "SELECT userNick FROM fishinglog.usertable WHERE userNick=%s"
        cur.execute(sql, userNick)

        if cur.rowcount > 0:
            # 이미 존재하는 경우
            return "FALSE"
        else:
            # 존재하지 않는 경우
            return "TRUE"

    except Exception as e:
        print(e)
        return "다시 한번 해주세요"

    finally:
        con.close()       

        
def UserLogin(userID, userPW):
    try:       
        con = pymysql.connect(host='localhost', user='root', password='1234',
                       db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')

        sql = "SELECT userNick FROM fishinglog.usertable WHERE userID=%s and userPW = %s"
    

        cur = con.cursor()  
        cur.execute(sql, (userID, userPW))
        result = cur.fetchone()[0]
        print(result)
        if result:
            # userNick 값 반환
            return result
        else:
            return "찾을수 없습니다"
        
    except Exception as e:
        print(e)
        return "다시 시도해주세요"
# STEP 5: DB 연결 종료
    finally:
        con.close() 
        

def LoginUserCheck(userID, userPW):
    #유저의 아이디와 비밀번호로 유저를 확인
    con = pymysql.connect(host='localhost', user='root', password='1234',
                    db='fishinglog', charset='utf8') # 한글처리 (charset = 'utf8')
    try:
        sql = "SELECT userNick FROM fishinglog.usertable where userID = '%s'and userPW = '%s'"

        cur = con.cursor()  
        cur.execute(sql, (userID, userPW))
        result = cur.fetchone() # 한 개의 row만 fetch
        return result # 결과 리턴
    except Exception as e:
        print(e)
        return "유저 정보를 알수없습니다"
    # STEP 5: DB 연결 종료
    finally:
        con.close()
        
