from voice_assistant.recorder import recording_stream
from voice_assistant.stream_asr import asr_sentence

stream = recording_stream(samplerate=16000, blocksize=512, channels=1)
print(asr_sentence(stream))
