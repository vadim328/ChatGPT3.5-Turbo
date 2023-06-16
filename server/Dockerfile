FROM python:3.9

# WORKDIR /code
# EXPOSE 8080
# COPY ./requirements.txt /code/requirements.txt
#
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
# COPY . /code

RUN mkdir /server
# COPY protobufs/ /service/protobufs/
COPY server/ /server/server/
WORKDIR /server/server
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt




CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
