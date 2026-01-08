FROM jrottenberg/ffmpeg:6.0-ubuntu

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python3", "bot.py"]
