FROM python:3.7-alpine

ADD . /tornado
WORKDIR /tornado
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python","main.py"]
