
FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

COPY kosr ./
COPY testdata ./
COPY templates ./
COPY evaluate.py ./
COPY train.py ./
#COPY ffmpeg.exe ./
#RUN chown daemon:daemon -R ffmpeg.exe

WORKDIR /home/ujlee/Templates/Speech_disorder/recognition

ADD . /home/ujlee/Templates/Speech_disorder/recognition



RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt


EXPOSE 80


CMD ["python", "app.py"]