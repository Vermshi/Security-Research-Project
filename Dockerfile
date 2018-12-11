FROM python:slim
COPY . /app
WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y gcc && pip --version && apt-get install libffi-dev && apt-get install openssl && pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD python ./src/flaskGUI.py

