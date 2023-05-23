FROM python:3.10

WORKDIR /app

COPY requirements.txt ./

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

COPY *.py /app
COPY static /app/static

EXPOSE 7000
CMD [ "python", "server.py" ]
