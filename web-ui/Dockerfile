FROM python:3.7-alpine

ADD . /tornado 
# skipp add command additional to volume is not possible because the volume mapping is done later in the tool chain and the files like requirements.txt are needed during the image build
WORKDIR /tornado
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","main.py"]

