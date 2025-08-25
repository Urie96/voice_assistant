import logging
import subprocess
from typing import Iterator


def stream_play(mp3_stream: Iterator[bytes]):
    ffmpeg_process = subprocess.Popen(
        [
            "ffplay",
            "-autoexit",
            "-nodisp",
            "-i",
            "-",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )  # initialize ffmpeg to decode mp3
    logging.info("mp3 audio player is started")

    if ffmpeg_process.stdin is None:
        return

    first = True

    for data in mp3_stream:
        if first:
            logging.info("mp3 audio player get first mp3 frame")
            first = False
        try:
            ffmpeg_process.stdin.write(data)
            ffmpeg_process.stdin.flush()
        except subprocess.CalledProcessError as e:
            # Capturing ffmpeg exceptions, printing error details
            logging.error(f"An error occurred: {e}")

    try:
        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()
        logging.info("mp3 audio player is stopped")
    except subprocess.CalledProcessError as e:
        # Capturing ffmpeg exceptions, printing error details
        logging.error(f"An error occurred: {e}")
