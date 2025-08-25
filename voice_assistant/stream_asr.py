import logging
import time
from typing import Any, Dict, Iterator, cast

import numpy as np
from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult
from numpy.typing import NDArray


class StreamASRCallback(RecognitionCallback):
    def __init__(self):
        self.complete = False
        self.err: str | None = None
        self.text: str | None = None
        super().__init__()

    def on_open(self) -> None:
        logging.info("RecognitionCallback open")
        pass

    def on_close(self) -> None:
        logging.info("RecognitionCallback close")
        pass

    def on_complete(self) -> None:
        logging.info("RecognitionCallback completed")
        pass

    def on_error(self, result: RecognitionResult) -> None:
        logging.info("RecognitionCallback error: ", result.message)
        self.complete = True
        self.err = result.message

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        sentence = cast(Dict[str, Any], sentence)
        if "text" in sentence:
            self.text = sentence["text"]
            logging.info("RecognitionCallback text: %s" % sentence["text"])
            if RecognitionResult.is_sentence_end(sentence):
                logging.info(
                    "RecognitionCallback sentence end, request_id:%s, usage:%s"
                    % (result.get_request_id(), result.get_usage(sentence))
                )
                self.complete = True


def transform(data: NDArray[np.float64]):
    if len(data.shape) == 2:
        data = data[:, 0]
    data = np.clip(data, -1.0, 1.0)
    return (data * 32767).astype(np.int16)


def _batch(stream: Iterator[NDArray[np.float64]]):
    buffer = []
    for data in stream:
        buffer.append(transform(data).tobytes())
        if len(buffer[0]) * len(buffer) >= 1024 * 12:
            # 一次收集100ms的数据
            yield b"".join(buffer)
            buffer = []


def asr_sentence(stream: Iterator[NDArray[np.float64]]):
    callback = StreamASRCallback()
    recognition = Recognition(
        model="paraformer-realtime-v2",
        format="pcm",
        sample_rate=16000,
        callback=callback,
    )
    recognition.start()

    first = True

    start = time.time()

    try:
        for data in _batch(stream):
            if first:
                logging.info("asr engine get first audio frame response")
                first = False
            if callback.complete:
                recognition.stop()
                return callback.text
            elif time.time() - start > 5 and callback.text is None:
                logging.info("[asr engine] no voice input in 5s, stopping")
                recognition.stop()
                return None
            else:
                recognition.send_audio_frame(data)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
