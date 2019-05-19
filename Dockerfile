FROM python:3

RUN mkdir /code

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000
ENTRYPOINT uvicorn --host "0.0.0.0" server:app