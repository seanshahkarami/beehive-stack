FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y python-pip python-dev

ADD requirements.txt /app/requirements.txt
ADD app.py /app/app.py
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]
