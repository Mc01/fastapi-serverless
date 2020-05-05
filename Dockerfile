FROM lambci/lambda:build-python3.7

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
