FROM python:3.9

RUN mkdir /server

COPY server/ /server/server/

WORKDIR /server/server

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
