FROM python:3.9


ADD ml_serv/requirements.txt .

RUN  apt-get update  && apt-get upgrade -y
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1


#RUN apt-get install -y python3 --fix-missing
#RUN apt-get install -y python3-pip --fix-missing
#RUN pip3 install --default-timeout=100 -U pip
#RUN pip3 install --default-timeout=100 --upgrade pip
#RUN pip3 install torch==2.0.0+cpu torchvision==0.15.1+cpu torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu
#RUN pip3 download -d .pipcache -r ./app/requirements.txt
#RUN pip3 install -r /requirements.txt
#RUN pip wheel --default-timeout=100 --wheel-dir  /wheels -r ./requirements.txt 

RUN apt-get install -y libgl1-mesa-dev
RUN pip3 download --cache-dir ./tmp/pipcache -r requirements.txt
#RUN pip install  -r  requirements.txt
RUN pip3 install --cache-dir ./tmp/pipcache -r requirements.txt

#FROM python:3.9




#COPY --from=builder /wheels /wheels
#COPY --from=builder /requirements.txt .
#
#RUN pip install --no-cache /wheels/*
COPY ./ml_serv/ /app

ENTRYPOINT ["python", "/app/main.py"]

#RUN python /app/main.py