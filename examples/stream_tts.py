import time

from voice_assistant.audio_player import _stream_play
from voice_assistant.stream_tts import stream_tts


def delayed_iterator(iterable, delay=1.0):
    for item in iterable:
        time.sleep(delay)  # 每次迭代前延迟
        print(item)
        yield item


mp3_stream = stream_tts(
    delayed_iterator(
        iter(
            [
                "默认采样率",
                "代表当前模型的最佳采样率",
                "，缺省条件下默认按照该采样率输出",
                "，同时支持降采样或升采样。",
                "如知妙音色，默认采样率16 kHz",
                "，使用时可以降采样到8 kHz，但升采样到48 kHz时不会有额外效果提升。",
            ]
        ),
        delay=2.0,
    )
)
_stream_play(mp3_stream)
