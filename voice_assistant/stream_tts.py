import logging
import queue
import threading
from typing import Iterator

from dashscope.audio.tts_v2 import ResultCallback, SpeechSynthesizer


class SpeechSynthesizerCallback(ResultCallback):
    def __init__(self, mp3_stream: queue.Queue[bytes | None]) -> None:
        super().__init__()
        self.queue = mp3_stream
        self.get_first = False

    def on_data(self, data: bytes) -> None:
        if not self.get_first:
            logging.info("tts engine get first mp3 frame response")
            self.get_first = True
        self.queue.put(data)

    def on_error(self, message: str):
        self.queue.put(None)
        logging.error(f"speech synthesis task failed, {message}")

    def on_complete(self) -> None:
        self.queue.put(None)
        logging.info("speech synthesis task completed")
        pass


def queue_iterator(q: queue.Queue[bytes | None]):
    """将队列转换为迭代器的生成器函数"""
    while True:
        item = q.get()
        if item is None:
            return
        yield item
        q.task_done()


def stream_tts(text_stream: Iterator[str]):
    mp3_stream: queue.Queue[bytes | None] = queue.Queue(maxsize=2)

    synthesizer_callback = SpeechSynthesizerCallback(mp3_stream)

    synthesizer = SpeechSynthesizer(
        model="cosyvoice-v2",
        voice="longling_v2",
        callback=synthesizer_callback,
    )

    def send_to_remote():
        first = True
        for chunk in text_stream:
            if first:
                logging.info("tts engine get first text chunk from upstream")
                first = False
            synthesizer.streaming_call(chunk)
        synthesizer.streaming_complete()

    threading.Thread(target=send_to_remote).start()

    return queue_iterator(mp3_stream)
