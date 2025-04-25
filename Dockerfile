FROM python:3.12-slim-buster

WORKDIR /app

COPY /requirements.txt /app

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y build-essential
RUN pip install -r /app/requirements.txt

COPY . /app

CMD ["streamlit", "run", "app.py"]