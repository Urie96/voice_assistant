import logging
from typing import Iterator

import numpy as np
import soundfile as sf
from numpy.typing import NDArray


class SentenceRecorder:
    def __init__(
        self,
        recording_stream: Iterator[NDArray[np.float64]],
        silence_secs: float,
        rate: int,
        threshold: float,
    ):
        self.stream = recording_stream
        self.recording = []
        self.silent_chunks = 0
        self.threshold = threshold  # 音量阈值，越小越敏感
        self.silence_limit = silence_secs * rate  # 连续多少秒低于阈值就停止
        self.rate = rate

    def _batch(self):
        buffer = []
        for data in self.stream:
            buffer.append(data)
            if buffer[0].shape[0] * len(buffer) / self.rate >= 0.5:
                # 一次收集0.5s的数据
                yield np.concatenate(buffer, axis=0)
                buffer = []

    def _is_silent_chunk(self, data: NDArray[np.float64]):
        volume = np.sqrt(np.mean(data**2))
        return volume < self.threshold

    def _save_wav(self, filename: str):
        recording = np.concatenate(self.recording, axis=0)
        sf.write(filename, recording, self.rate)
        logging.info(f"录音已保存到 {filename}")

    def wait_wav_path(self):
        for data in self._batch():
            self.recording.append(data)
            if self._is_silent_chunk(data):
                self.silent_chunks += data.shape[0]
            else:
                self.silent_chunks = 0

            if self.silent_chunks >= self.silence_limit:
                logging.info("检测到静音", self.silent_chunks, self.silence_limit)
                self.silent_chunks = 0
                return self._save_wav("output.wav")


if __name__ == "__main__":
    from .recorder import recording_stream

    stream = recording_stream(samplerate=16000, blocksize=512, channels=1)
    sr = SentenceRecorder(stream, silence_secs=2, rate=16000, threshold=0.05)
    print(sr.wait_wav_path())
