#Docker image with python 3.7 and opencv 4.1.0
FROM jjanzic/docker-python3-opencv

WORKDIR /app 
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]