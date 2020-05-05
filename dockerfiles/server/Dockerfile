FROM python:3.8
ADD ducc /ducc/
ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
CMD ["python", "-m", "ducc.server", "run-server", "-h", "0.0.0.0", "rabbitmq://localhost:5672/"]
