import logging

from voice_assistant.recorder import recording_stream
from voice_assistant.wake_word import WakeWord

stream = recording_stream(samplerate=16000, blocksize=512, channels=1)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

wakeup = WakeWord(stream, threshold=0.5)
while True:
    name = wakeup.wait()
    print(name)
