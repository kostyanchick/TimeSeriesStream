FROM python:3.7

# set the working directory to /app
WORKDIR /app

ADD . /app

RUN pip install -r /app/requirements.txt

EXPOSE 8081

CMD [ "python", "./run.py" ]