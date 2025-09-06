import logging

import sys
from voice_assistant import start

# 配置日志格式，包含时间
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def tts():
    import sys

    from voice_assistant.audio_player import AudioPlayer
    from voice_assistant.stream_tts import stream_tts

    print("tts mode start")

    audio_player = AudioPlayer()

    for line in sys.stdin:
        mp3_stream = stream_tts(iter(line))
        audio_player.play(mp3_stream, wait=False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tts":
        tts()
    else:
        start()
