FROM python:3.8
ADD ducc /ducc/
ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
CMD ["python", "-m", "ducc.gui", "run-server", "-h", "0.0.0.0", "--database", "mongodb://localhost:27017/"]
