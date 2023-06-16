FROM python

RUN mkdir /service

COPY bot/ /service/bot/

WORKDIR /service/bot

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py"]