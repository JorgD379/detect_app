FROM python:3

WORKDIR /solution
COPY . .

# dependencies
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
        build-essential git python3 python3-pip

RUN pip3 install -U pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

#RUN mim install mmcv==2.0.0 # can be deleted

CMD /bin/sh -c "python3 main.py"
