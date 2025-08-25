import logging
from typing import Iterator, cast

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage


def iter_with_log(it: Iterator[str]):
    chunks = []
    for item in it:
        if len(chunks) == 0:
            logging.info(f"get first agent resp chunk: {item}")
        chunks.append(item)
        yield item
    logging.info(f"agent resp complete, resp: {''.join(chunks)}")


class VoiceAgent:
    def __init__(self):
        self.model = init_chat_model("deepseek-chat", model_provider="deepseek")
        self.system_prompt = "你叫金宝，是一个闲聊型语音 AI 助手，主要任务是和用户展开日常性的友善聊天。请不要回复使用任何格式化文本，回复要求口语化，不要使用markdown格式或者列表，不要以“哎呀”开头。"

    def stream(self, question):
        resp = self.model.stream(
            [SystemMessage(self.system_prompt), HumanMessage(question)]
        )
        s = (chunk.content for chunk in resp)
        return iter_with_log(cast(Iterator[str], s))
