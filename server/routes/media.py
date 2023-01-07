import tempfile
import secrets
from pathlib import Path

import aiofile
from fastapi import APIRouter, UploadFile, Request, Response, status, BackgroundTasks, Form
from fastapi.responses import FileResponse

from server.tasks.media import optimize

router = APIRouter()


@router.get('/media/{filename}')
async def get_media(filename: str, request: Request):
    media_path = Path('media/', filename)
    spoof_suffixes = ('.mp4', '.webm', '.mov', '.png', '.jpg', '.mp3', '.aac', '.opus', '.ogg', '.m4a')
    asvid_suffixes = ('.mp3', '.aac', '.opus', '.ogg', '.m4a')

    # Is the file a video or image?
    if Path(request.url.path).suffix in spoof_suffixes:
        # Is Discord probing the file?
        if 'Discordbot' in request.headers.get('user-agent'):
            # Is this video or audio?
            if Path(request.url.path).suffix in asvid_suffixes:
                spoof_path = Path(media_path.parent, media_path.stem + '.asvid.mp4')
            else:
                spoof_path = Path(media_path.parent, media_path.stem + '.thumb' + media_path.suffix)

            if not spoof_path.exists():
                return FileResponse(media_path)
            return FileResponse(spoof_path)

        # Are we missing the 'Accept' header? (likely Discord too)
        if 'Accept' not in request.headers.keys():
            if Path(request.url.path).suffix in asvid_suffixes:
                spoof_path = Path(media_path.parent, media_path.stem + '.asvid.mp4')
            else:
                spoof_path = Path(media_path.parent, media_path.stem + '.thumb' + media_path.suffix)

            if not spoof_path.exists():
                return FileResponse(media_path)
            return FileResponse(spoof_path)

    return FileResponse(media_path)


@router.post('/media')
async def post_media(file: UploadFile, response: Response,
                     background_tasks: BackgroundTasks, password: str = Form()):
    # FIXME: Add a database or something!!
    if not secrets.compare_digest(password, "test_password"):
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    temp_path = Path(tempfile.gettempdir()) / f"tmp_{secrets.token_hex(8)}"
    final_name = f'{secrets.token_hex(8)}{Path(file.filename).suffix}'
    async with aiofile.async_open(temp_path, 'wb') as f:
        await f.write(await file.read())

    response.status_code = status.HTTP_202_ACCEPTED
    background_tasks.add_task(optimize, temp_path, final_name)
    return {"expected_name": final_name}