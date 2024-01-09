#!/usr/bin/env python3

from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller
from enum import Enum

# Local imports
from brawlhalla_bot_merrittlj.util import logging_utils

listener = keyboard.Listener()


def _for_canonical(func):  # Returns a lambda function that "translates" the argument(key) cannonically, and passes it into the original passed function.
    return lambda key: func(listener.canonical(key))

class Hotkey:
    def __init__(self, key_combination = '<ctrl>+x', activated_func = lambda : logging_utils.logpr(f"Hotkey {self._key_combination} activated.")):
        self._key_combination = key_combination
        self._activated_func = activated_func

    def run(self):
        """
        "Runs" the hotkey, as in starts listening for hotkey key combination presses.
        """
        
        hotkey = keyboard.HotKey(keyboard.HotKey.parse(self._key_combination), self._activated_func)
        
        with keyboard.Listener(on_press = _for_canonical(hotkey.press), on_release = _for_canonical(hotkey.release)) as listener:
            listener.wait()
            logging_utils.logpr(f"Hotkey {self._key_combination} ready to run.\n")
            listener.join()
