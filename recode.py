import pymysql
import wave
import sounddevice as sd
from datetime import datetime
import boto3
import pymysql
from playsound import playsound
import pyttsx3   



def select_speech_Id(user_Id , s3_file_path):
    conn = pymysql.connect(

    host='project-db-stu3.smhrd.com', 
    user='Insa4_IOTB_final_3', 
    password='aischool3',
    db='Insa4_IOTB_final_3', 
    charset='utf8', port=3307
    )
    cursor = conn.cursor()


    sql = """select speak_Id from t_Speech where user_id = %s and speak_Content = %s"""


    # 예시: SQL 쿼리 실행 (테이블 이름을 원하는 테이블로 변경해야 합니다.)
    try:

        cursor.execute(sql, (user_Id,s3_file_path))
        result = cursor.fetchall()        
        conn.commit()
        conn.close()
        result = result[0][0]

        return result
    except:
        print("select error")
        return 1

def record_and_save_wav(file_path, duration=60, sample_rate=44100):
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
    AWS_ACCESS_KEY = "AKIAUXQ6F3NS2S6S2UN3"
    AWS_SECRET_ACCESS_KEY = "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"
    AWS_S3_BUCKET_NAME = "gjaischool-intelb-tec-audio-storage"
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

def Speech_input(user_Id,s3_file_path):
    # MySQL 연결 설정
    conn = pymysql.connect(

    host='project-db-stu3.smhrd.com', 
    user='Insa4_IOTB_final_3', 
    password='aischool3',
    db='Insa4_IOTB_final_3', 
    charset='utf8', port=3307
    )
    cursor = conn.cursor()

    try:
        # 데이터베이스에 삽입
        sql = """INSERT INTO t_Speech (user_Id, speak_Content) VALUES (%s, %s)"""
        cursor.execute(sql, (user_Id, s3_file_path))
            
        # 변경사항 커밋
        conn.commit()
        print("PCM 데이터가 MySQL에 성공적으로 저장되었습니다.")
        conn.close()
    except:
        print("error")
        conn.close()

def input_STT_TTS(user_id, speak_id, Output_text):

    conn = pymysql.connect(

    host='project-db-stu3.smhrd.com', 
    user='Insa4_IOTB_final_3', 
    password='aischool3',
    db='Insa4_IOTB_final_3', 
    charset='utf8', port=3307
    )
    cursor = conn.cursor()


    try:
        sql = """INSERT INTO t_TTS (user_Id, speak_Id, text_Content) VALUES (%s,%s,%s)"""
        # 예시: SQL 쿼리 실행 (테이블 이름을 원하는 테이블로 변경해야 합니다.)
        cursor.execute(sql, (user_id,speak_id, Output_text))
        # 변경사항 커밋
        conn.commit()
        conn.close()
        print("Stt 삽입끝")
    except:
        print("STT에러")
        conn.close()

def text_to_speech(text):
    # voice_dict = {'남': 0, '여': 1}
    # code = voice_dict[gender]
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[code].id)
    engine.say(text)
    engine.runAndWait()
    
