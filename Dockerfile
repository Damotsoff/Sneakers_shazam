FROM python:3.8

WORKDIR /app

COPY /req.txt /app/req.txt

ENV TELEGRAM_TOKEN="5064465837:AAGMzrZHz0Eg6AiQ2FoDAk0HTZh2uQ5ZpfU"
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN python3.8 -m pip install -U pip
RUN python3.8 -m pip install -r /app/req.txt

COPY . /app

ENTRYPOINT [ "python3.8", "/bot/bot.py" ]