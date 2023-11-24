from flask import Flask, jsonify, Blueprint, redirect, request, render_template, send_from_directory, session, url_for, flash
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
import wave
import sounddevice as sd
import pyaudio
from datetime import datetime
import boto3
import pymysql
from playsound import playsound
import pyttsx3   

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


@app.route('/')
def main():
    if 'user' in session:
        user = session['user']
        user_Name = user['user_Name']
        return render_template('/main/index.html', message = user_Name)
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
    query = "SELECT * FROM t_User where user_Id = %s and user_Pwd = %s"
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
    
    cur.execute("INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) VALUES (%s, %s, CONCAT(%s,%s,%s), %s, %s, %s, LPAD(%s, 4, '0'), %s, %s, %s, %s, %s, %s, %s, %s);",
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
        

@app.route('/mypage/update', methods=["POST"])
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
        query = "UPDATE t_User SET user_Phone1=%s, user_Phone2=%s, user_Phone3=%s, user_Phone=CONCAT(%s,%s,%s), user_Pwd=%s, user_Disability=%s, user_PostNumber=%s, user_Address=%s, user_Details=%s, user_Year=LPAD(%s, 4, '0'), user_Region=%s WHERE user_Id=%s"
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
        
        return redirect(url_for('main', user_Name = user_Name, user_Phone = user_Phone))

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
    


def record_and_save_wav(file_path, duration=10, sample_rate=44100):
    # 녹음 설정
    recording = sd.rec(int(sample_rate * duration),
                       samplerate=sample_rate, channels=2, dtype='int16')

    sd.wait()

    # WAV 파일로 저장
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())

def wav_to_pcm(input_wav, output_pcm):
    with wave.open(input_wav, 'rb') as wav_file:
        # WAV 파일의 포맷 정보 가져오기
        params = wav_file.getparams()

        # PCM 파일로 쓰기
        with open(output_pcm, 'wb') as pcm_file:
            # WAV 파일 헤더를 제외한 데이터를 PCM 파일에 쓰기
            pcm_file.write(wav_file.readframes(params.nframes))


def S3_input_data(formatted_now):
    AWS_ACCESS_KEY = "AKIAUXQ6F3NS2FCBDBMS"
    AWS_SECRET_ACCESS_KEY = "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"
    AWS_S3_BUCKET_NAME = "gjaischool-aiot-bcalss-tec-audio2"
    print("S3_OPEN!")
    # S3 클라이언트를 생성합니다.

    try:
        s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY, 
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        local_file_path = "./instance/output.pcm"
        s3_file_path =f"user/{formatted_now}.pcm"

        # 파일을 S3에 업로드합니다.
        s3.upload_file(local_file_path, AWS_S3_BUCKET_NAME, s3_file_path)

        print(f"{s3_file_path} 업로드가 완료되었습니다.")
        s3.close()
        print("S3_CLOSE!")
        return s3_file_path
    except:
        s3.close()
        return print("S3_error")

def S3_outut_data(formatted_now):
    AWS_ACCESS_KEY = "AKIAUXQ6F3NS2FCBDBMS"
    AWS_SECRET_ACCESS_KEY = "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"
    AWS_S3_BUCKET_NAME = "gjaischool-aiot-bcalss-tec-audio2"

    # S3 클라이언트를 생성합니다.
    s3 = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        # 다운로드할 로컬 파일 경로를 설정합니다.
        local_download_path = f"./instance/download/{formatted_now}.pcm"
        print(local_download_path)
        # S3 키를 설정하면서 폴더 경로를 포함시킵니다.
        s3_key = f"user/{formatted_now}.pcm"
        print(s3_key)
        # 파일을 S3에서 다운로드합니다.
        s3.download_file(AWS_S3_BUCKET_NAME, s3_key, local_download_path)
        print(f"{AWS_S3_BUCKET_NAME}/{s3_key}을(를) {local_download_path}로 다운로드했습니다.")
        s3.close()
        print("s3_close")
    except:
        s3.close()
        print("error_s3_close")


# 실행
if __name__ == '__main__':
    # app.run(debug=False, host="0.0.0.0")
    app.run(debug=True, host="")
