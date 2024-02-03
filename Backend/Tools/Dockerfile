FROM python:3.8-slim-buster
RUN apt-get update && \
    apt-get install rabbitmq-server -y 
RUN apt-get install -y clustalo
RUN apt-get install -y default-libmysqlclient-dev
WORKDIR /Tools
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ ./
RUN chmod +x ./start.sh
EXPOSE 8000
CMD ["./start.sh"]



