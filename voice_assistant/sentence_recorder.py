import numpy as np
import soundfile as sf
import sounddevice as sd


class SentenceRecorder:
    def __init__(
        self,
        silence_limit,
        threshold,
    ):
        self.recording = []
        self.silent_chunks = 0
        self.threshold = threshold  # 音量阈值，越小越敏感
        self.silence_limit = silence_limit  # 连续多少秒低于阈值就停止

    def write(self, data):
        self.recording.append(data)
        volume = np.sqrt(np.mean(data**2))
        if volume < self.threshold:
            self.silent_chunks += 1
        else:
            self.silent_chunks = 0

        if self.silent_chunks >= self.silence_limit:
            print("检测到静音")
            return True
        return False

    def save_wav(self, filename, rate):
        recording = np.concatenate(self.recording, axis=0)
        sf.write(filename, recording, rate)
        print(f"录音已保存到 {filename}")


if __name__ == "__main__":
    with sd.InputStream(
        samplerate=16000, channels=1, blocksize=int(16000 * 0.5)
    ) as stream:
        print("开始录音")
        sentence_recorder = SentenceRecorder(silence_limit=4, threshold=0.1)

        while True:
            data, _ = stream.read(int(16000 * 0.5))
            if sentence_recorder.write(data):
                sentence_recorder.save_wav("sentence.wav", 16000)
                break
