import logging
import sounddevice as sd


def recording_stream(samplerate: int, blocksize: int, channels=1):
    logging.info("开始录音...")
    with sd.InputStream(
        samplerate=samplerate, channels=channels, blocksize=blocksize
    ) as stream:
        while True:
            data, _ = stream.read(blocksize)
            yield data
