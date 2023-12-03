from flask import Flask, jsonify, Blueprint, redirect, request, render_template, send_from_directory, session, url_for, flash, send_file
from flask_mysqldb import MySQL
import pymysql
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
import secrets
import os
# import wave
# import sounddevice as sd
from datetime import datetime
# import boto3
# from playsound import playsound
import pyttsx3
# import recode
from flask_cors import cross_origin
# import voiceAPI
# from pydub import AudioSegment
# import evaluate



app = Flask(__name__, static_url_path='/static')
app.secret_key = secrets.token_hex(16)

# render_template : 동적(dynamic) template directory 로 이동 // send_from_directory : 정적(static) directory 로 이동

# connection = pymysql.connect(host='',  port = 3307, user = ) # 아래와 동일

app.config['MYSQL_HOST'] = 'project-db-stu3.smhrd.com'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'Insa4_IOTB_final_3'
app.config['MYSQL_PASSWORD'] = 'aischool3'
app.config['MYSQL_DB'] = 'Insa4_IOTB_final_3'

mysql = MySQL(app)

@app.route('/test')
def test():
    # if 'user' in session:
    #     user = session['user']
    #     user_Name = user['user_Name']
    #     user_Gender = user['user_Gender']
        # return render_template('/record3.html', user_Name = user_Name, user_Gender=user_Gender)
    # else:
        return render_template('/record3.html')

@app.route('/')
def main():
    if 'user' in session:
        user = session['user']
        user_Name = user['user_Name']
        user_Gender = user['user_Gender']
        return render_template('/main/index.html', user_Name = user_Name, user_Gender = user_Gender)
    else:
        return render_template("/main/index.html")


@app.route('/user/mypage')
def mypage():
    user = session.get('user')
    if user: # 로그인된 상태
        if user.get('user_Id') != "admin":
            return render_template('/user/mypage.html', **user)
        else:
            return render_template('/user/mypage.html')


@app.route('/user/registerForm')
def registerForm():
    return render_template('/user/register.html')

@app.route('/user/loginForm')
def loginForm():
    return render_template('/user/login.html')


@app.route('/user/login', methods = ['POST'])
def login():
    user_Id = request.form.get('user_Id')
    user_Pwd = request.form.get('user_Pwd')
    
    cur = mysql.connection.cursor()
    query = "SELECT * FROM t_User where user_Id = %s and user_Pwd = SHA(%s)"
    cur.execute(query, (user_Id, user_Pwd))
    result = cur.fetchone()
   
    mysql.connection.commit()
    cur.close()
    
    if result:
        (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, 
        user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, 
        user_PostNumber, user_Address, user_Details) = result

        # flash('로그인 완료', category='success')
        
        keys = ['user_Name', 'user_Id', 'user_Phone', 'user_Pwd', 'user_Gender', 'user_Disability', 
                'user_Year', 'user_Region', 'user_Phone1', 'user_Phone2', 'user_Phone3', 'user_Date', 
                'user_PostNumber', 'user_Address', 'user_Details']
        user = dict(zip(keys, result))
        session['user'] = user
        flash('로그인 완료', category = 'success')


        session['user_Phone'] = user_Phone # 세션에 user_Phone 정보 기입

        return jsonify({'message': 'success', 'user_Name': user_Name}), 200
    else:
        return jsonify({'message': 'failed'}), 401
        

            
# 회원가입 처리
@app.route('/user/register', methods = ['POST'])
def register():
    user_Name = request.form.get('user_Name')
    user_Id = request.form.get('user_Id')
    user_Phone1 = request.form.get('user_Phone1')
    user_Phone2 = request.form.get('user_Phone2')
    user_Phone3 = request.form.get('user_Phone3')
    user_Pwd = request.form.get('user_Pwd')
    user_Gender = request.form.get('user_Gender')
    user_Disability = request.form.get('user_Disability')
    user_Date = request.form.get('user_Date')
    user_PostNumber = request.form.get('user_PostNumber')
    user_Address = request.form.get('user_Address')
    user_Details = request.form.get('user_Details')
    

    # 문자열을 datetime객체로 반환
    # from datetime import datetime
    # # 날짜 문자열을 datetime 객체로 변환
    # date_object = datetime.strptime(user_Date, '%Y-%m-%d')

    # # 연도 추출
    # user_Year = int(date_object.strftime('%Y'))
    # user_Year = "%04d" % user_Year
    # user_Year = int()
    
    user_Date = request.form.get('user_Date')  # 선택한 날짜 가져오기
    user_Year = user_Date.split('-')[0]  # 날짜에서 연도 추출
    user_Year = int(user_Year)
    
    # 지역추출
    user_Region = user_Address.split(' ')[0]
 
    
    cur = mysql.connection.cursor()
    
    cur.execute("INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) VALUES (%s, %s, CONCAT(%s,%s,%s), SHA(%s), %s, %s, LPAD(%s, 4, '0'), %s, %s, %s, %s, %s, %s, %s, %s);",
                (user_Name, user_Id, user_Phone1, user_Phone2, user_Phone3, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details))
    
    mysql.connection.commit()

    query = "SELECT * FROM t_User where user_Id = %s and user_Pwd = %s"
    cur.execute(query, (user_Id, user_Pwd))
    result = cur.fetchone()

    cur.close()

    user = {'user_Name':user_Name, 'user_Id':user_Id, 'user_Phone':user_Phone1+user_Phone2+user_Phone3, 'user_Pwd':user_Pwd, 'user_Gender':user_Gender, 'user_Disability':user_Disability, 'user_Year':user_Year, 'user_Region':user_Region, 'user_Phone1':user_Phone1, 'user_Phone2':user_Phone2, 'user_Phone3':user_Phone3, 'user_Date':user_Date, 'user_PostNumber':user_PostNumber, 'user_Address':user_Address, 'user_Details':user_Details}
    session['user'] = user

    if result: # 로그인 코드와 동일
        (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, 
        user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, 
        user_PostNumber, user_Address, user_Details) = result

        # flash('로그인 완료', category='success')
        
        keys = ['user_Name', 'user_Id', 'user_Phone', 'user_Pwd', 'user_Gender', 'user_Disability', 
                'user_Year', 'user_Region', 'user_Phone1', 'user_Phone2', 'user_Phone3', 'user_Date', 
                'user_PostNumber', 'user_Address', 'user_Details']
        user = dict(zip(keys, result))
        session['user'] = user
        flash('로그인 완료', category = 'success')

        session['user_Phone'] = user_Phone # 세션에 user_Phone 정보 기입
    
    return redirect(url_for('main', user_Name = user_Name))
    


# 폰번호 중복검사
@app.route('/user/check_phone', methods=['GET'])
def check_phone():
    user_Phone = request.args.get('user_Phone') # database에 있는 폰번호 불러오기
    
    if not user_Phone:
        return jsonify({'RESULT': 'False', 'message': '폰번호를 입력해 주세요.'})
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_User WHERE user_Phone = %s;", (user_Phone,))
    data = cur.fetchone()
    cur.close()
    
    if data:
        # 이미 폰번호가 이미 존재합니다.
        return jsonify({'RESULT': 'NotFound', 'message': '이미 사용중인 번호입니다.'})
    else:
        # 중복된 폰번호가 없습니다.
        return jsonify({'RESULT': 'Found', 'message': '사용 가능한 번호입니다.'})


# 아이디 중복검사
@app.route('/user/check_id', methods=['GET'])
def check_id():
    user_Id = request.args.get('user_Id') # database에 있는 아이디 불러오기

    if not user_Id:
        return jsonify({'result': 'False', 'message': '아이디를 입력해 주세요.'})

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_User WHERE user_Id = %s;", (user_Id,))
    data = cur.fetchone()
    cur.close()

    if data:
        # 아이디가 이미 존재합니다.
        return jsonify({'result': 'False', 'message': '이미 사용중인 아이디입니다.'})
    else:
        # 중복된 아이디가 없습니다.
        return jsonify({'result': 'True', 'message': '사용 가능한 아이디입니다.'})

@app.route('/user/logout')
def logout():

    # session.pop('user',None)
    session.clear()
    flash('로그아웃 완료', category='success')
    return redirect('/')
        

@app.route('/user/update', methods=["POST"])
def update():
    user=session.get('user')
    if user:

        user_Name = user.get('user_Name')
        user_Id = user.get('user_Id')
        user_Phone1 = request.form.get('user_Phone1')
        user_Phone2 = request.form.get('user_Phone2')
        user_Phone3 = request.form.get('user_Phone3')
        user_Pwd = request.form.get('user_Pwd')
        user_Gender = user.get('user_Gender')
        user_Disability = request.form.get('user_Disability')
        user_Date = user.get('user_Date')
        user_PostNumber = request.form.get('user_PostNumber')
        user_Address = request.form.get('user_Address')
        user_Details = request.form.get('user_Details')


        user_Date = request.form.get('user_Date')  # 선택한 날짜 가져오기

        from datetime import datetime

        user_Date = datetime.strptime(user_Date, '%a, %d %b %Y %H:%M:%S %Z')
        user_Date = user_Date.strftime('%Y-%m-%d')
        user_Year = user_Date.split('-')[0]  # 날짜에서 연도 추출
        user_Year = int(user_Year)
        
        # 지역추출
        user_Region = user_Address.split(' ')[0]


        cur = mysql.connection.cursor()
        query = "UPDATE t_User SET user_Phone1=%s, user_Phone2=%s, user_Phone3=%s, user_Phone=CONCAT(%s,%s,%s), user_Pwd=SHA(%s), user_Disability=%s, user_PostNumber=%s, user_Address=%s, user_Details=%s, user_Year=LPAD(%s, 4, '0'), user_Region=%s WHERE user_Id=%s"
        cur.execute(query, (user_Phone1, user_Phone2, user_Phone3, user_Phone1, user_Phone2, user_Phone3, user_Pwd, user_Disability, user_PostNumber, user_Address, user_Details, user_Year, user_Region, user_Id))


        mysql.connection.commit()

        cur.close()

        cur = mysql.connection.cursor()
        query = "SELECT * FROM t_User where user_Id = %s and user_Pwd = %s"
        cur.execute(query, (user_Id, user_Pwd))
        result = cur.fetchone()

        mysql.connection.commit()
        cur.close()
        
        if result:
            (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, 
            user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, 
            user_PostNumber, user_Address, user_Details) = result
            keys = ['user_Name', 'user_Id', 'user_Phone', 'user_Pwd', 'user_Gender', 'user_Disability', 
                    'user_Year', 'user_Region', 'user_Phone1', 'user_Phone2', 'user_Phone3', 'user_Date', 
                    'user_PostNumber', 'user_Address', 'user_Details']
            user = dict(zip(keys, result))
            session['user'] = user

            session['user_Phone'] = user_Phone # 세션에 user_Phone 정보 기입

            flash('로그인 완료', category = 'success')
        
        return redirect(url_for('main', user_Name = user_Name))


@app.route('/user/leave')
def leave():
    user = session.get('user')
    if user:
        user_Id = user.get('user_Id')
        cur = mysql.connection.cursor()
        query = "DELETE FROM t_User WHERE user_Id = %s"
        cur.execute(query, (user_Id,))
        mysql.connection.commit()
        cur.close()
        session.clear()
        flash('로그아웃 완료', category='success')

        return redirect(url_for('main'))
    else:
        return redirect(url_for('main'))



# Output_text = "" # 전역 변수 선언
# import urllib3
# import json
# import base64
# import speech_recognition as sr

# # 연습용 레코드
# @app.route('/record/start', methods = ['POST'])
# def start():
#     user = session.get('user')
#     if user:
#         user_Id = user.get('user_Id')
        
        
        # r = sr.Recognizer()
        # with sr.Microphone() as source:
        #     audio = r.listen(source)
        
        # try:
        #     speech_text = r.recognize_google(audio, language='ko')
        #     return speech_text
        # except sr.UnknownValueError:
        #     print("Speech Recognition could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
        # openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
        # accessKey = "57536e54-f9a7-4f44-9a3a-998b3692fba2"
        # file_path = "./instance/hello.wav"
        # languageCode = "korean"

        # file = open(file_path, "rb")
        # audioContents = base64.b64encode(file.read()).decode("utf8")
        # file.close()

        # requestJson = {    
        # "argument": {
        #     "language_code": languageCode,
        #     "audio": audioContents
        # }
        # }

        # # REST API
        # http = urllib3.PoolManager()
        # response = http.request(
        # "POST",
        # openApiURL,
        # headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
        # body=json.dumps(requestJson)
        # )

        # print("[responseCode] " + str(response.status))
        # print("[responBody]")
        # # print(str(response.data,"utf-8"))
        # data = json.loads(response.data.decode("utf-8", errors='ignore'))    
        # Output_text = data['return_object']['recognized']
        
        
    ## docker 모델적용해서 Output_text
    # output_pcm_file = './instance/output.pcm'
    # predict = evaluate.mains(output_pcm_file)
    
    # Output_text = "해당 문구를 TTS로 호출하시오."
    
    # return Output_text # 변환된 텍스트를 반환
    # return predict[0]


@app.route('/record/save', methods = ['POST'])
def save():
    try:
        if request.method == 'POST':
            user = session.get('user')
            user_Id = user['user_Id']
            
            # 클라이언트로부터 전송된 오디오 데이터를 받음
            # file_path = './instance/recorded_audio.wav' # 녹음본 파일경로
            # audio_data = request.files['audio']
            # audio_data.save(file_path)
            # WAV 파일로 저장
            # with open(file_path, 'wb') as f:
                # f.write(audio_data)
                
            # recode.record_and_save_wav(file_path)
            # output_pcm_file = './instance/output.pcm' # 모델에 사용가능한 음성파일 (.pcm) 경로
            # recode.wav_to_pcm(file_path, output_pcm_file) # 음성 녹음본 -> 모델에 사용가능한 음성파일
            now = datetime.now()
            formatted_now = now.strftime("%Y_%m_%d_%H_%M_%S")
            print(formatted_now)

            # # PCM 파일 변환이후에 S3_input 으로 data 올림
            # s3_file_path = recode.S3_input_data(formatted_now) # S3 저장소에 데이터(pcm 파일) 저장
            # recode.Speech_input(user_Id , s3_file_path) # 저장된 파일경로가 DB (MySQL)에 저장
            # # S3 에서 DATA 받아오는거 DB에서 저장된거 Select 해올것! 
            # speak_id = recode.select_speech_Id(user_Id , s3_file_path)
            
            return jsonify({'status': 'success', 'message': '오디오 녹음이 성공적으로 완료되었습니다.'})
        else:
            return jsonify({'status': 'error', 'message': '올바른 HTTP 메소드가 아닙니다.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'오류: {str(e)}'})

# @app.route('/record/play')
# def play():
#     # 저장된 녹음 파일을 읽어서 응답으로 전송
#     with open(file_path, 'rb') as f:
#         audio_data = f.read()
    
#     return audio_data

def text_to_speech(text):
    # voice_dict = {'남': 0, '여': 1}
    # code = voice_dict[gender]
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[code].id)
    engine.say(text)
    engine.runAndWait()

@app.route('/record/tts', methods = ['POST'])
@cross_origin()
def TTS():
    try:
        if request.method == 'POST':
            data = request.get_json()  # JSON 데이터를 파싱
            text = data['text']  # 'text' 키로 데이터에 접근
            # gender = data['gender']
            text_to_speech(text)
            # text = request.form['speech']
            # gender = request.form['voices']
            # text_to_speech(text, gender)

            #text = start()
            #tts = recode.text_to_speech(text)
            #recode.text_to_speech(Output_text) # start() 함수에서 반환된 값을 매개변수로 사용
            #return render_template('record3.html')
            # text_to_speech("안녕하세요")
            return jsonify({'status': 'success', 'message': '오디오 녹음이 성공적으로 완료되었습니다.'})
        else:
            return jsonify({'status': 'error', 'message': '올바른 HTTP 메소드가 아닙니다.'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'오류: {str(e)}'})
            

    

# @app.route('/record', methods=['POST'])
# def record():
#     user = session.get('user')
#     if user: # 로그인 상태
#         user_Id = user.get('user_Id')
#         file_path = './instance/recorded_audio.wav' # 녹음본 파일경로
#         recode.record_and_save_wav(file_path) # 녹음 후 음성파일(.wav) 저장
#         output_pcm_file = './instance/output.pcm' # 모델에 사용가능한 음성파일 (.pcm) 경로
#         recode.wav_to_pcm(file_path, output_pcm_file) # 음성 녹음본 -> 모델에 사용가능한 음성파일
#         now = datetime.now()
#         formatted_now = now.strftime("%Y_%m_%d_%H_%M_%S")
#         print(formatted_now)
#         # PCM 파일 변환이후에 S3_input 으로 data 올림
#         s3_file_path = recode.S3_input_data(formatted_now) # S3 저장소에 데이터(pcm 파일) 저장
#         recode.Speech_input(user_Id , s3_file_path) # 저장된 파일경로가 DB (MySQL)에 저장

#         # S3 에서 DATA 받아오는거 DB에서 저장된거 Select 해올것! 
#         speak_id = recode.select_speech_Id(user_Id , s3_file_path) 
        
#         Output_text = "안녕하세요?" # pcm파일을 모델로 적용한 Text
#         recode.text_to_speech(Output_text) # python 전용 TTS
#         recode.input_STT_TTS(user_Id, speak_id, Output_text) # STT/TTS 를 DB에 저장
#         return jsonify({'status': 'success', 'message': '오디오가 성공적으로 녹음되었습니다'})


# import speech_recognition as sr

# def get_audio():
#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         transcript = " "

    
#     try:
#         transcript = r.recognize_google(audio, language="ko-KR")
#         print("Speech Recognition thinks you said: ", transcript)
#     except sr.UnknownValueError:
#         print(" Speech Recognition colud not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
#     return render_template('test.html', transcript=transcript)
    
# @app.route('/render')
# def rendering():
#     return render_template('/user/speech.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     audio_file = request.files['audio']
#     audio_file.save(os.path.join('./instance', 'recorded_audio.wav'))
#     return '', 204 # No content

# 실행
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")