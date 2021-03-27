FROM ubuntu:20.04

COPY . /backend
COPY requirements.txt /requirements.txt

RUN apt-get update \
    && apt-get install python3-dev python3-pip -y \
    && pip3 install -r requirements.txt

ENV PYTHONPATH=/backend
WORKDIR /backend

EXPOSE 3000


ENTRYPOINT ["uvicorn"]
CMD ["app.app:app", "--host", "0.0.0.0"]