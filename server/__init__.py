from pathlib import Path

from fastapi import FastAPI

from server.routes import media


app = FastAPI()


app.include_router(media.router)

# create media directory if doesnt exist
Path("media/").mkdir(exist_ok=True)


@app.get("/")
async def root():
    return {"hello": "world"}