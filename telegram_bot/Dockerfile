FROM python:3.9


ADD telegram_bot/requirements.txt .

RUN  apt-get update  && apt-get upgrade -y


RUN apt-get install -y libgl1-mesa-dev
RUN pip3 download --cache-dir ./tmp/pipcache -r requirements.txt

RUN pip3 install --cache-dir ./tmp/pipcache -r requirements.txt

COPY ./telegram_bot/ /app

ENTRYPOINT ["python", "/app/bot.py"]

#RUN python /app/main.py