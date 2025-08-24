from dashscope.audio.asr import Recognition

recognition = Recognition(
    model="paraformer-realtime-v2",
    format="wav",
    sample_rate=16000,
    callback=None,
)


def asr(wav_path):
    result = recognition.call(wav_path)
    sentence_list = result.get_sentence()
    if sentence_list is None:
        print("No result")
        return None
    else:
        print("The brief result is:  ")
        for sentence in sentence_list:
            text = sentence["text"]
            print(text)
            return text


if __name__ == "__main__":
    print("asr: ", asr("./sentence.wav"))
