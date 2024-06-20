from vosk import Model, KaldiRecognizer
from pathlib import Path
from typing import Union
import logging
import pyaudio
import json
import time
import os

from src.basic_commands.controller import WordToCommand


logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parent

WordToCommand = WordToCommand()


class VoiceRecognizer:

    def __init__(self,
            model_dir: Union[str, None] = BASE_DIR.joinpath("models"),
            model_path: str = "vosk-model-small-ru-0.4",
            rate: int = 16000,
            frames_per_buffer: int = 8000
        ):
        """
            model_dir: Path to a directory with models
            model_path: Name of model (if model_dir is specified) else Full path of model
        """

        if model_dir:
            self.model_path = os.path.join(model_dir, model_path)
        else:
            self.model_path = model_path

        self.model = Model(self.model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
        self.stream.start_stream()

        self.last_time_said = None


    def listen(self, num_frames: int = 400, exception_on_overflow: bool = False):
        timout_time  = 10

        while True:
            if self.last_time_said and (time.time() - self.last_time_said) >= timout_time:
                WordToCommand.is_talking = False
                self.last_time_said = None

            data = self.stream.read(num_frames, exception_on_overflow)
            if self.rec.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.rec.Result())
                if answer['text']:
                    self.last_time_said = time.time()

                    yield answer['text']


def recognition(model_dir: str):
    recognizer = VoiceRecognizer(
                            model_dir,
                            # "vosk-model-ru-0.10"
                        )

    text = recognizer.listen()
    for word in text:
        logger.info(f"Распознано: {word}")

        index, keys = WordToCommand.recognize(word)
        if not index or not keys:
            continue

        WordToCommand.call_command(index, keys)
