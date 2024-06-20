from typing import Tuple, Any, Union
from difflib import SequenceMatcher
from pathlib import Path
import logging
import json
import os

from src.keyboard.controller import Keyboard


logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parent
UPPER_DIR = BASE_DIR.parent.parent
INDEXES_FILE = BASE_DIR.joinpath("indexes.json")


Keyboard = Keyboard()


class WordToCommand:
    def __init__(self):
        if os.name == "nt":
            self.is_mac = False
        else:
            self.is_mac = True

        if self.is_mac == True:
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


    def find_index_by_word(self, word: str) -> Tuple[Union[None, str], Union[None, list[str]]]:
        with open(INDEXES_FILE, encoding='utf-8') as file:
            data = json.loads(file.read())

        match = {}
        for index in data:
            for index_word in data[index].get("words"):
                if word == index_word:
                    return index, data[index].get("keys")
                else:
                    ratio = SequenceMatcher(None, word, index_word).ratio()
                    if not match.get('ratio') or ratio > match["ratio"]:
                        match["ratio"] = ratio
                        match["index"] = index
                        match["keys"] = data[index].get("keys")

        if not match.get('ratio'):
            return None, None
        else:
            if match.get('ratio') > 0.7:
                # if match.get("ratio") > 0.9:
                #     data[match["index"]].append(word)

                return match.get("index"), match.get("keys")

        return None, None


    def recognize(self, text: str) -> Tuple[Union[None, str], Union[str, None]]:
        index, keys = self.find_index_by_word(text)

        if index and keys:
            return index, keys
        else:
            return None, None


    def call_command(self, index: str, keys: list[str]):
        # if index == "index_0":
        for key in keys:
            Keyboard.press(key)
