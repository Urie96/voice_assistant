import sounddevice as sd
import numpy as np
import openwakeword
from openwakeword.model import Model

# Get microphone stream
CHANNELS = 1
RATE = 16000
CHUNK = 512

openwakeword.utils.download_models()


class WakeWord:
    def __init__(self, callback, threshold=0.5):
        self.model = Model(inference_framework="onnx")
        self.threshold = threshold
        self.callback = callback
        pass

    def write(self, data) -> None:
        if len(data.shape) == 2:
            data = data[:, 0]
        if data.dtype == np.float32:
            data = np.clip(data, -1.0, 1.0)
            data = (data * 32767).astype(np.int16)
        prediction = self.model.predict(data)
        for name, prob in prediction.items():
            if prob > self.threshold:
                print(f"Wake word: {name}, score={prob:.2f}")
                self.callback(name)
                self.model.reset()


if __name__ == "__main__":
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, blocksize=CHUNK) as stream:
        print("#" * 100)
        print("Listening for wakewords...")
        print("#" * 100)
        wake_word = WakeWord(callback=lambda name: print(f"callback: {name}"))

        while True:
            data, _ = stream.read(CHUNK)
            wake_word.write(data[:, 0])
