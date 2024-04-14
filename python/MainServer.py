import base64
import io
import os
from threading import Thread
from tokenize import generate_tokens
import zipfile
from flask import Flask, request, jsonify, send_file
import json
from datetime import datetime, timedelta
import DB.DB_TEST as DB
import ocean_Weather_insert as Ocean_Weather
import schedule
import time
from io import BytesIO
from PIL import Image, ExifTags
import gzip
import requests         


app = Flask(__name__)
#프로필 변경
@app.route('/select_profile', methods=['POST'])
def select_profile():
    json_str = request.form['UploadJsonData']
    data_dict = json.loads(json_str)
    #게시글 정보 추출
    user_Nick = data_dict['user_Nick']
    #post_id = DB.user_post(latitude, longitude, date, text, user_Nick, user_Location)
    result = DB.Select_Profile(user_Nick)
    
    if(result == None):
        result = "default"
        
    response = {'result': result}  # result를 리스트로 변환
    print(response)
    return jsonify(response), 200


#프로필 변경
@app.route('/upload_Pfrofile', methods=['POST'])
def upload_Pfrofile():
    json_str = request.form['UploadJsonData']
    data_dict = json.loads(json_str)
    #게시글 정보 추출
    user_Nick = data_dict['user_Nick']
        
    #post_id = DB.user_post(latitude, longitude, date, text, user_Nick, user_Location)
  
    for i in range(1, len(request.files) + 1):
        file_key = 'image_{}'.format(i)
        if file_key not in request.files:
            return jsonify({'error': 'no {} uploaded'.format(file_key)}), 400
        image = request.files[file_key]
        upload_folder = "C:\\Users\\MM\\Desktop\\user_profile"
        image_name = generate_unique_filename()
        image_path = os.path.join(upload_folder, image_name)
        image.save(image_path)
        fix_image_orientation(image_path)
        width, height = get_image_size(image_path)
        if(width>height):
            resize_and_save_image(image, image_path,1920, 1080)
        elif(width<height):
            resize_and_save_image(image, image_path, 1080, 1920)

        DB.upload_Pfrofile(image_name,user_Nick)
        response = {'result': image_name}  # result를 리스트로 변환

        #print(image_url)
        
    return jsonify(response), 200

#좋아요 불러오기 
@app.route('/Post_Like_Load', methods=['POST'])
def Post_Like_Load():
    #게시글 확인하기
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)

            user_nick = data_dict['user_nick']

            result = DB.like_load(user_nick)

            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)
            response = {'result': "asdf"}
            return jsonify(response), 200

#좋아요 기능 
@app.route('/post_like', methods=['POST'])
def Post_Like():
    #게시글 확인하기
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)

            post_id = data_dict['post_id']
            like_type = data_dict['like_type']
            user_nick = data_dict['user_nick']
            result = DB.update_like(post_id,like_type, user_nick)
            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)
            response = {'result': "asdf"}
            return jsonify(response), 200

#댓글 확인하기 
@app.route('/select_post_comment', methods=['POST'])
def select_post_comment():
    #게시글 확인하기
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)

            post_id = data_dict['post_id']

            result = DB.select_post_comment(post_id)

            response = {'result': result}  # result를 리스트로 변환

            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)
            response = {'result': "asdf"}
            return jsonify(response), 200

#댓글 입력하기 
@app.route('/post_comment', methods=['POST'])
def Post_Comment():
    #게시글 확인하기
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)
            user_comment = data_dict['user_comment']
            post_id = data_dict['post_id']
            user_nick = data_dict['user_nick']
            result = DB.user_post_comment(user_comment,post_id,user_nick)
            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)
            response = {'result': "asdf"}
            return jsonify(response), 200

#포스트 삭제하기 
@app.route('/delete_post', methods=['POST'])
def Delete_Post():
    #게시글 확인하기
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)
            post_id = data_dict['post_id']
            result = DB.delete_post(post_id)
            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)


#마이페이지
@app.route('/MyPage', methods=['GET','POST'])
def MyPage():
    #게시글 확인하기
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
        
            data_dict = json.loads(json_str)
            user_id = data_dict['user_id']
            user_nick = data_dict['user_nick']
            result1 = DB.MyPage(user_id)
            result2 = DB.My_Post_Like(user_nick)
            response = {'MyPage': result1, 'post_like' : result2}  # result를 리스트로 변환

            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)


# banned_fish = "C:\\Users\\MM\\Desktop\\banned_fish"
# # 이미지 파일에 액세스할 엔드포인트
# @app.route('/banned_fish/<image_filename>')
# def get_banned_fish_image(image_filename):
#     try:
#         image_path = os.path.join(banned_fish, image_filename)
#         return send_file(image_path, as_attachment=True)
#     except Exception as e:
#         return str(e)
    
#낚시팁 
@app.route('/Fishing_Tip', methods=['GET','POST'])
def Fishing_Tip():
    #게시글 확인하기
    if request.method == 'GET':
        try:
            result = DB.Search_Fishing_Tip()
            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)

#금어기 확인
@app.route('/fish_banned', methods=['GET', 'POST'])
def Fish_Banned():
    #게시글 확인하기
    if request.method == 'GET':
        try:
            result = DB.Fish_Ban()
            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)
            
    if request.method == 'POST':
        json_str = request.form['UploadJsonData']
        
        data_dict = json.loads(json_str)

        if(data_dict['type'] == "Search_Now_banned_fish"):
            try:
                result = DB.Search_Now_banned_fish()
                response = {'result': result}  # result를 리스트로 변환
                return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

            except Exception as e:
                print(e)
        elif(data_dict['type'] == "Search_CM_banned_fish"):
            try:
                result = DB.Search_CM_banned_fish()
                response = {'result': result}  # result를 리스트로 변환
                return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

            except Exception as e:
                print(e)


#어종분석 확인
@app.route('/Fish_Species_Analysis', methods=['POST'])
def Fish_Species_Analysis():
    #게시글 확인하기
    if request.method == 'POST':
        openApiURL = "https://2maargjyfo.apigw.ntruss.com/fishlens/v1/predict"
        accessKey = "loo6kTk4fhCZlTsOViFdChUtzyOmtbawdpl7gA4J"
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)
            for i in range(1, len(request.files) + 1):
                file_key = 'image_{}'.format(i)
                if file_key not in request.files:
                    return jsonify({'error': 'no {} uploaded'.format(file_key)}), 400
                image = request.files[file_key]
                upload_folder = "C:\\Users\\MM\\Desktop\\qwer"
                #image_path = os.path.join(upload_folder, image.filename)
                image_name = generate_unique_filename()
                image_path = os.path.join(upload_folder, image_name)
                image.save(image_path)
            
            file = {'file': open(image_path, 'rb')}
            headers = {"x-ncp-apigw-api-key": accessKey}
            response = requests.post(openApiURL, headers=headers, files=file)
            # 응답 확인
            data = json.loads(response.text)
            wikidata = DB.SelectFishWiki(data['detail'][0]['국명'])
            # if(list(data['detail']).count):
            #     response = {'result': "다시 시도해주세요"}
            response = {'result': wikidata} 
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)


def generate_unique_filename():
    import uuid
    return str(uuid.uuid4()) + '.jpg'

def allowed_file(filename):
    # 허용된 파일 확장자 확인
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:

            width, height = img.size
            return width, height
    except Exception as e:
        print(f"Error: {e}")
        return None

def fix_image_orientation(image_path):
    try:
        with Image.open(image_path) as img:
            # 이미지가 Exif 데이터를 가지고 있는지 확인
            if hasattr(img, "_getexif") and img._getexif() is not None:
                exif = dict(img._getexif().items())

                # Exif 데이터에서 회전 정보를 가져오기
                orientation = exif.get(274, 1)

                # 회전 정보에 따라 이미지 회전
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

                # 회전된 이미지를 저장
                img.save(image_path, quality=100)

    except Exception as e:
        print(f"Error fixing image orientation: {e}")
        
def resize_and_save_image(image, output_path, max_width, max_height):
    try:
        with Image.open(image) as img:
            if hasattr(img, "_getexif") and img._getexif() is not None:
                exif = dict(img._getexif().items())

                # Exif 데이터에서 회전 정보를 가져오기
                orientation = exif.get(274, 1)

                # 회전 정보에 따라 이미지 회전
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
            # 이미지 크기를 비율에 맞게 조정
                img.thumbnail((max_width, max_height))
                img.save(output_path)
    except Exception as e:
        print(f"Error resizing and saving image: {e}")

#이미지 받고 업로드
@app.route('/upload_image', methods=['POST'])
def upload_image():
    json_str = request.form['UploadJsonData']
    data_dict = json.loads(json_str)

    #게시글 정보 추출
    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    date = data_dict['date']
    text = data_dict['text']
    user_Location = data_dict['user_Location']
    user_Nick = data_dict['user_Nick']

        
    post_id = DB.user_post(latitude, longitude, date, text, user_Nick, user_Location)
  
    for i in range(1, len(request.files) + 1):
        file_key = 'image_{}'.format(i)
        if file_key not in request.files:
            return jsonify({'error': 'no {} uploaded'.format(file_key)}), 400
        image = request.files[file_key]
        upload_folder = "C:\\Users\\MM\\Desktop\\test"
        image_name = generate_unique_filename()
        image_path = os.path.join(upload_folder, image_name)
        image.save(image_path)
        fix_image_orientation(image_path)
        width, height = get_image_size(image_path)
        if(width>height):
            resize_and_save_image(image, image_path,1920, 1080)
        elif(width<height):
            resize_and_save_image(image, image_path, 1080, 1920)
        DB.user_post_image(image_path, post_id, image_name)
        image_url = f'http://yourserver.com/images/{image_name}'  # 이미지 URL 생성
        #print(image_url)
        
    return jsonify({'message': 'Image uploaded successfully', 'image_urls': [image_url]}, 200)


# image_folder = "C:\\Users\\MM\\Desktop\\test"
# # 이미지 파일에 액세스할 엔드포인트
# @app.route('/images/<image_filename>')
# def get_image(image_filename):
#     try:
#         image_path = os.path.join(image_folder, image_filename)
#         return send_file(image_path, as_attachment=True)
#     except Exception as e:
#         return str(e)
    
    
# fish_image_folder = "C:\\Users\\MM\\Desktop\\fishwiki"
# # 이미지 파일에 액세스할 엔드포인트
# @app.route('/fishwiki/<image_filename>')
# def get_fish_image(image_filename):
#     try:
#         image_path = os.path.join(fish_image_folder, image_filename)
#         return send_file(image_path, as_attachment=True)
#     except Exception as e:
#         return str(e)
    
#게시글 확인
@app.route('/View_Post', methods=['GET','POST'])
def View_Post():
    #게시글 확인하기
    if request.method == 'GET':
        try:
            result = DB.View_Post_GET()

            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)
    if request.method == 'POST':
        try:
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)

            post_id = data_dict['post_id']

            result = DB.View_Post_POST(post_id)

            response = {'result': result}  # result를 리스트로 변환
            return jsonify(response), 200#, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print(e)


#날씨정보 전송
@app.route('/Marine_Weather', methods=['POST'])
def Marine_Weather():
    # 
    if request.method == 'POST':
        json_str = request.form['UploadJsonData']
        data_dict = json.loads(json_str)
        beach_name = data_dict['beach_name']

        try:
            result = DB.Marine_Weather(beach_name)
            response = {'result': list(result)}  # result를 리스트로 변환
            return jsonify(response), 200, {'Content-Type': 'application/json; charset=utf-8'}

        except Exception as e:
            print("error" + e)
            return result
            #response = {'status': 'success', 'token': token}
            #return jsonify(response), 200



#회원가입
@app.route('/signup', methods=['POST'])
def signup():
    # 클라이언트에서 회원가입 정보를 전송한 경우
    if request.method == 'POST':
        json_str = request.form['UploadJsonData']
        data_dict = json.loads(json_str)
        # 회원 정보 추출
        userID = data_dict['ID']
        userPW = data_dict['PW']
        userNick = data_dict['Nickname']
        try:
            result = DB.UserSignup(userID,userPW,userNick)
            return result
        except Exception as e:
            print("error" + e)
            return result
            #response = {'status': 'success', 'token': token}
            #return jsonify(response), 200
            
#로그인          
@app.route('/login', methods=['POST'])
def login():
    # 클라이언트에서 회원가입 정보를 전송한 경우
    if request.method == 'POST':
        json_str = request.form['UploadJsonData']
        data_dict = json.loads(json_str)
        # 회원 정보 추출
        userID = data_dict['ID']
        userPW = data_dict['PW']
        try:    
            print(userID)
            print(userPW)
            result = DB.UserLogin(userID,userPW)
            print(result)
            return result, 200
        except Exception as e:
            print("error" + e)
            return result
            #response = {'status': 'success', 'token': token}
            #return jsonify(response), 200
      
#아이디 중복체크  
@app.route('/idckeck', methods=['POST'])
def idckeck():
    try:
    # 클라이언트에서 회원가입 정보를 전송한 경우
        if request.method == 'POST':
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)

        # 회원 정보 추출
            userID = data_dict['ID']
            result = DB.CkeckUserID(userID)
    except Exception as e:
            print(e)
            print("mainerror")
    
    return result

#닉네임 중복체크
@app.route('/nickcheck', methods=['POST'])
def nickcheck():
    try:
    # 클라이언트에서 닉네임 정보를 전송한 경우
        if request.method == 'POST':
            json_str = request.form['UploadJsonData']
            data_dict = json.loads(json_str)

        # 회원 정보 추출
            userNick = data_dict['Nickname']
            check = DB.CkeckUserNick(userNick)
    except Exception as e:
            print(e)
            print("mainerror")
    
    return check

#테스트용
@app.route('/',methods=['GET','POST'])
def server_test():
    # 작동시 글을 보내줌

    return "Hello, World!", 200


def periodic_function():
    Ocean_Weather.Marine_Weather_Data()


if __name__ == '__main__':
    app_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    app_thread.daemon = True
    app_thread.start()

    # 오전 11시에 함수 실행 예약
    schedule.every().day.at("21:20").do(periodic_function)

    while True:
        schedule.run_pending()  # 예약된 작업 실행
        time.sleep(1)
    