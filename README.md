# yga-fastapi

A little backend thing I made for my website, so I can embed large files and audio on Discord.

this slightly differs from my other, now archived "yga-flask" because it uses fastapi, 
and the file isn't immediately available on upload

instead it does some processing to troll discord into loading videos faster and showing audio as video.
this is done with ffmpeg. it doesn't require much CPU unless someone uploads 40 albums at once or smth

TODO:
* Add database support 
* Add documentation

# installing
For docker: Installing goes something like this
```shell
$ git clone https://github.com/000yesnt/yga-fastapi.git
$ cd yga-fastapi
$ docker build -t yga-fastapi .
$ docker run -dp 9876:9876 --name yga-fastapi_1 \
    -v yga-fastapi_media:/media --tmpfs /tmp \
    yga-fastapi:latest
```
Running directly:  make sure you have `ffmpeg` and at least Python 3.10.
Python 3.11 is recommended as that's what the dockerfile builds from.
```shell
$ git clone https://github.com/000yesnt/yga-fastapi.git
$ cd yga-fastapi
$ python3 -m venv .env && .env/bin/activate
$ pip install -r requirements.txt
$ uvicorn server:app --host 0.0.0.0 --port 9876
```

The server runs on port 9876. Nothing else is required (for now)