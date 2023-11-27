FROM python:3.9
# FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

COPY instance ./
COPY static ./ 
COPY kosr ./ 
COPY testdata ./
COPY templates ./
COPY evaluate.py ./
COPY train.py ./
COPY speaker.sql ./
COPY recode.py ./



#COPY ffmpeg.exe ./
#RUN chown daemon:daemon -R ffmpeg.exe

WORKDIR /home/ujlee/Templates/Speech_disorder/recognition

ADD . /home/ujlee/Templates/Speech_disorder/recognition


RUN apt-get update -y && apt-get install -y --no-install-recommends \
                                        build-essential \
                                        gcc \
                                        libsndfile1 \ 
                                        pkg-config \
                                        ffmpeg \
                                        libportaudio2 \
                                        libasound2-dev \
                                        portaudio19-dev \
                                        default-libmysqlclient-dev \ 
                                    && rm -rf /var/lib/apt/lists/*

#  && rm -rf /var/lib/apt/lists/* : 설치 후 불필요한 패키지 리스트 삭제하는 명령어 (도커 이미지를 최적화하는데 기여)
# MySQL 개발 라이브러리 설치

# 필요한 시스템 패키지 설치

RUN pip install --no-cache-dir -r eunbi_requirements.txt

# RUN apt-get install pkg-config
RUN pip install --upgrade pip
# RUN pip install -r eunbi_requirements.txt
EXPOSE 80


CMD ["python", "app.py"]

# FROM python:3.9.13
# FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

# COPY instance ./
# COPY static ./
# COPY kosr ./
# COPY testdata ./
# COPY templates ./
# COPY evaluate.py ./
# COPY train.py ./
# COPY speaker.sql ./
# COPY recode.py ./

# #COPY ffmpeg.exe ./
# #RUN chown daemon:daemon -R ffmpeg.exe

# WORKDIR /home/ujlee/Templates/Speech_disorder/recognition

# ADD . /home/ujlee/Templates/Speech_disorder/recognition


# RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
#                                         libsndfile1 pkg-config

# # RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
# #                                        libsndfile1 libmysqlclient-dev 

# # RUN apt-get install -y --no-install-recommends build-essential gcc  pkg-config 
# # RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 libmysqlclient-dev

# RUN pip install --upgrade pip
# RUN pip install --trusted-host pypi.python.org -r eunbi_requirements.txt

# # 버전관리 requirements 생성 : pip freeze > 파일명

# EXPOSE 80


# CMD ["python", "app.py"]