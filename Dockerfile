FROM python:3.6

MAINTAINER clooooode<jackey8616@gmail.com>

EXPOSE 5000

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py", "--host=0.0.0.0", "--port=5000", "--db-host=redis"]
