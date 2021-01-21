FROM python:3.8-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY /backend /usr/src/app
RUN pip install -r requirements.txt
EXPOSE 8000

CMD [ "python", "run.py" ]
