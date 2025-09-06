import logging
import queue
import subprocess
import threading
from typing import Iterator


def _stream_play(mp3_stream: Iterator[bytes]):
    ffmpeg_process = subprocess.Popen(
        [
            "ffplay",
            "-autoexit",
            "-nodisp",
            # "-fflags",
            # "nobuffer",
            "-i",
            "-",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )  # initialize ffmpeg to decode mp3
    logging.info("mp3 audio player is started")

    assert ffmpeg_process.stdin

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
        logging.info("mp3 audio play is stopping")
        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()
        logging.info("mp3 audio player is stopped")
    except subprocess.CalledProcessError as e:
        # Capturing ffmpeg exceptions, printing error details
        logging.error(f"An error occurred: {e}")


class AudioPlayer:
    def __init__(self):
        self._queue: queue.Queue[tuple[Iterator[bytes], threading.Event | None]] = (
            queue.Queue()
        )
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

    def _worker(self):
        while True:
            audio_stream, done_event = self._queue.get()
            _stream_play(audio_stream)
            self._queue.task_done()
            if done_event:
                done_event.set()

    def play(self, stream: Iterator[bytes], wait: bool = True):
        if wait:
            done_event = threading.Event()
            self._queue.put((stream, done_event))
            done_event.wait()  # 阻塞直到播放完成
        else:
            self._queue.put((stream, None))
