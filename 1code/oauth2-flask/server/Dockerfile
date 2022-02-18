FROM python:3.8

RUN mkdir -p /home/server
WORKDIR /home/server
COPY ./requirements.txt /home/server/requirements.txt

#COPY ./sources.list /etc/apt/sources.list

#RUN apt-get update
#RUN apt-get install apt-uitls -y
#RUN apt-get install build-essential libssl-dev libffi-dev python-dev -y
RUN pip install --upgrade pip
RUN pip install cryptography -i https://pypi.douban.com/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install mysql-connector-python -i https://pypi.tuna.tsinghua.edu.cn/simple
