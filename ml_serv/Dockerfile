FROM python:3.9-slim as builder


ADD ml_serv/requirements.txt ./app


RUN apt-get update && apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get install -y python3 --fix-missing
RUN apt-get install -y python3-pip --fix-missing
			

RUN pip3 install -U pip
RUN pip3 install --upgrade pip
RUN pip3 install torch==2.0.1+cpu torchvision==0.15.1+cpu torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip wheel --default-timeout=100 --wheel-dir  /app/wheels -r ./app/requirements.txt 



FROM python:3.9-slim

WORKDIR /app

WORKDIR /app
COPY . ./

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

CMD /app -c "python3 main.py"