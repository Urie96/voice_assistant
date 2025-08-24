from dashscope import Generation


class LLM:
    def __init__(self):
        self.system_prompt = "你是一个闲聊型语音AI助手，主要任务是和用户展开日常性的友善聊天。请不要回复使用任何格式化文本，回复要求口语化，不要使用markdown格式或者列表。"

    def ask(self, question):
        responses = Generation.call(
            model="qwen-plus",
            messages=messages,
            result_format="message",
            stream=True,
            incremental_output=True,
        )
