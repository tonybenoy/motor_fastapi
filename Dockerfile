FROM python:latest
RUN apt update -y
RUN apt upgrade -y

ADD ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
ENV MONGODB_URL=${MONGODB_URL}
COPY src/ /src
#CMD ["gunicorn", "-b 0.0.0.0:8000","src.main:app", "-w 1", "-k uvicorn.workers.UvicornWorker", "--preload"]