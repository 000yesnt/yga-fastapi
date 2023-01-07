import shutil
from os import PathLike
from pathlib import Path

import ffmpeg
from PIL import Image


def optimize(temp: PathLike | str, filename: str):
    # FIXME: Explain wtf is going on here
    media_dest = Path('media/', filename)
    thumb_dest = Path('media/', media_dest.stem + '.thumb' + media_dest.suffix)
    audio_dest = Path('media/', media_dest.stem + '.asvid.mp4')
    audio_bg = Path('assets/audio-bg.png')

    video_suffixes = ('.mp4', '.webm', '.mov')
    faststart_suffixes = ('.mp4', '.mov')
    image_suffixes = ('.jpg', '.png', '.jpeg', '.jfif')
    audio_suffixes = ('.mp3', '.aac', '.opus', '.ogg', '.m4a')

    try:
        if media_dest.suffix in faststart_suffixes:
            # Faststart optimization for any compatible video
            (
                ffmpeg
                .input(temp)
                .output(media_dest.absolute(), codec='copy', shortest=None, movflags='faststart')
                .run()
                # ffmpeg -i in_file.mp4 -c copy -movflags +faststart -y media_dest.mp4
            )
        else:
            shutil.copy(temp, media_dest)

        if media_dest.suffix in video_suffixes:
            # Generate tiny videos to trick Discord into loading the video faster
            (
                ffmpeg
                .input(temp, t=0.003)
                .output(thumb_dest.absolute(), codec='copy')
                .run()
                # ffmpeg -t 00:00:00.003 -i in_file -c copy -y in_file.thumb.mp4"
            )
        elif media_dest.suffix in image_suffixes:
            # Same idea as previous if
            with Image.open(media_dest) as im:
                Image.new(mode='RGB', size=(im.width, im.height)).save(thumb_dest, quality=1, optimize=True)
        elif media_dest.suffix in audio_suffixes:
            # Make a video from the audio file so that embedded audio files are playable on discord
            (
                ffmpeg
                .input(audio_bg.absolute(), loop=1)
                .global_args('-i', temp)
                .output(filename=audio_dest.absolute(), shortest=None,
                        vcodec='libx264', movflags='faststart', r=4,
                        preset='ultrafast', crf=36, tune='stillimage', acodec='copy')
                .run()
                # command = (f"ffmpeg -loop 1 -i {audio_bg.absolute()} "
                #           f"-i {in_file.absolute()} "
                #           f"-c:v libx264 -tune stillimage -crf 36 -preset ultrafast -movflags +faststart -r 4 "
                #           f"-c:a copy "
                #           f"-shortest -y {audio_dest}")
            )

    finally:
        Path(temp).unlink()
