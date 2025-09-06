import logging
from .wake_word import WakeWord
from .stream_asr import asr_sentence
from .agent import VoiceAgent
from .recorder import recording_stream
from .stream_tts import stream_tts
from .audio_player import AudioPlayer


def start():
    recorder_stream = recording_stream(samplerate=16000, blocksize=1280)
    wake_word = WakeWord(recorder_stream, threshold=0.6)
    agent = VoiceAgent()
    audio_player = AudioPlayer()
    while True:
        wake_word.wait()
        user_msg = asr_sentence(recorder_stream)
        if user_msg is None or user_msg.strip() == "":
            logging.info("no voice input, session end")
            continue
        logging.info(f"user speak: {user_msg}")

        agent_resp_stream = agent.stream(user_msg)
        mp3_stream = stream_tts(agent_resp_stream)
        audio_player.play(mp3_stream)
        logging.info("session end")
