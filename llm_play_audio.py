#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

from http import HTTPStatus

from dashscope import Generation
from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback

from RealtimeMp3Player import RealtimeMp3Player

system_text = "你是一个闲聊型语音AI助手，主要任务是和用户展开日常性的友善聊天。请不要回复使用任何格式化文本，回复要求口语化，不要使用markdown格式或者列表。"
query_to_llm = "番茄炒鸡蛋怎么做？"


def synthesize_speech_from_llm_by_streaming_mode(query_text: str):
    """
    Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
    you can customize the synthesis parameters, like model, format, sample_rate or other parameters
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html

    """
    player = RealtimeMp3Player()

    # Define a callback to handle the result

    class Callback(ResultCallback):
        def on_open(self):
            pass

        def on_complete(self):
            pass

        def on_error(self, message: str):
            print(f"speech synthesis task failed, {message}")

        def on_close(self):
            pass

        def on_event(self, message):
            pass

        def on_data(self, data: bytes) -> None:
            # save audio to file
            player.write(data)
            # f.write(data)

    # Call the speech synthesizer callback
    synthesizer_callback = Callback()

    synthesizer = SpeechSynthesizer(
        model="cosyvoice-v2",
        voice="longling_v2",
        callback=synthesizer_callback,
    )

    # Prepare for the LLM call
    messages = [
        {"role": "system", "content": system_text},
        {"role": "user", "content": query_text},
    ]
    print(">>> query: " + query_text)
    responses = Generation.call(
        model="qwen-plus",
        messages=messages,
        result_format="message",  # set result format as 'message'
        stream=True,  # enable stream output
        incremental_output=True,  # enable incremental output
    )
    print(">>> answer: ", end="")
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            # send llm result to synthesizer
            llm_text_chunk = response.output.choices[0]["message"]["content"]
            print(llm_text_chunk, end="", flush=True)
            synthesizer.streaming_call(llm_text_chunk)
        else:
            print(
                "Request id: %s, Status code: %s, error code: %s, error message: %s"
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                )
            )
    synthesizer.streaming_complete()
    # add new line after llm outputs
    print("")
    print(">>> playback completed")
    print(
        "[Metric] requestId: {}, first package delay ms: {}".format(
            synthesizer.get_last_request_id(), synthesizer.get_first_package_delay()
        )
    )
    # stop realtime mp3 player
    player.stop()


# main function
if __name__ == "__main__":
    synthesize_speech_from_llm_by_streaming_mode(query_text=query_to_llm)
