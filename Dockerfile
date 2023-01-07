FROM python:3.11-slim
COPY requirements.txt ./

RUN apt-get update && apt-get upgrade -y && apt-get install -y ffmpeg
RUN pip3 install -r requirements.txt

COPY server/ ./server
COPY server/assets ./assets

EXPOSE 9876
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9876"]