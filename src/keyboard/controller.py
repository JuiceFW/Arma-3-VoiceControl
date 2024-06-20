from pathlib import Path
from typing import Union
import keyboard
import logging
import time


logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent



class Keyboard:
    def press(self, button: str):
        keyboard.press(button)
        time.sleep(.1)
        keyboard.release(button)
        time.sleep(.1)


    def hold(self, button: str, timeout: Union[int, None]):
        keyboard.press(button)
        if timeout:
            time.sleep(timeout)
            keyboard.release(button)
            time.sleep(.1)


    def release(self, button: str, timeout: Union[int, None]):
        keyboard.release(button)
        if timeout:
            time.sleep(timeout)
            keyboard.press(button)
            time.sleep(.1)
