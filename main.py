import sounddevice as sd
from llm_play_audio import synthesize_speech_from_llm_by_streaming_mode
from voice_assistant.wake_word import WakeWord
from voice_assistant.sentence_recorder import SentenceRecorder
from voice_assistant.audio_recognizer import asr

RATE = 16000  # 采样率
CHANNELS = 1  # 单声道
CHUNK = 512
block_duration = 0.5  # 每次读取 0.5 秒


def reply_user(user_msg):
    synthesize_speech_from_llm_by_streaming_mode(user_msg)


def main():
    print("开始录音...")

    with sd.InputStream(samplerate=RATE, channels=CHANNELS, blocksize=CHUNK) as stream:
        print("\n\n")
        print("#" * 100)
        print("Listening for wakewords...")
        print("#" * 100)

        def handle_session(wake_word):
            recorder = SentenceRecorder(silence_limit=4, threshold=0.1)
            while True:
                data, _ = stream.read(int(RATE * block_duration))
                if recorder.write(data):
                    recorder.save_wav("output.wav", RATE)
                    break

            user_msg = asr("./output.wav")
            reply_user(user_msg)

        wake_words = WakeWord(callback=handle_session)
        while True:
            data, _ = stream.read(CHUNK)
            wake_words.write(data)


if __name__ == "__main__":
    main()
