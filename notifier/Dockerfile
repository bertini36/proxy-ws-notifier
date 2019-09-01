FROM python:3.7

COPY . /data/notifier

RUN pip install -U pip
RUN pip install -r /data/notifier/requirements.txt

WORKDIR /data/notifier

CMD ["python", "./manage.py"]
