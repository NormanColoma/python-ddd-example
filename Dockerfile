FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src ./src
COPY app.py .
CMD [ "python3", "app.py"]

