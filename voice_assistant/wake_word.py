import logging
import platform
import time
from typing import Any, Iterator, cast

import numpy as np
from numpy.typing import NDArray
from openwakeword.model import Model

# openwakeword.utils.download_models()  # type: ignore


class WakeWord:
    def __init__(
        self,
        recording_stream: Iterator[NDArray[np.float64]],
        threshold,
    ):
        enable_speex_noise_suppression = False
        if platform.system().lower() == "linux":
            logging.info("enable speex noise suppression in linux")
            enable_speex_noise_suppression = True
        self.model = Model(
            wakeword_models=["./onnx/xiao_ai.onnx"],
            inference_framework="onnx",
            enable_speex_noise_suppression=enable_speex_noise_suppression,
        )
        self.threshold = threshold

        def transform(data):
            if len(data.shape) == 2:
                data = data[:, 0]
            data = np.clip(data, -1.0, 1.0)
            data = (data * 32767).astype(np.int16)
            return data

        self.stream = (transform(data) for data in recording_stream)
        pass

    def wait(self):
        logging.info("开始检测唤醒词...")
        self.model.reset()
        start = time.time()
        for data in self.stream:
            prediction = self.model.predict(data)
            prediction = cast(dict[str, Any], prediction)

            for name, prob in prediction.items():
                logging.debug(f"Wake word: {name}, score={prob:.2f}")
                if time.time() - start > 2 and prob > self.threshold:
                    logging.info(f"Wake word: {name}, score={prob:.2f}")
                    return name
