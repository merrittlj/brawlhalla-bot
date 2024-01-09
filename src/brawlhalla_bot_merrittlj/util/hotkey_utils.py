#!/usr/bin/env python3

from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller
import threading
from enum import Enum

# Local imports
# From ./(util/)
from brawlhalla_bot_merrittlj.util import logging_utils

listener = keyboard.Listener()


class Hotkey_Modes(Enum):
    ONESHOT = 1  # Runs the activation function every hotkey activation.
    TOGGLE = 2  # Toggles the activation function between running and not running.

def _for_canonical(func):  # Returns a lambda function that "translates" the argument(key) cannonically, and passes it into the original passed function.
    return lambda key: func(listener.canonical(key))

class Hotkey:
    def __init__(self, key_combination = '<ctrl>+x', activated_func = lambda : logging_utils.logpr(f"Hotkey {self._key_combination} activated."), hotkey_mode = Hotkey_Modes.ONESHOT):
        self._key_combination = key_combination
        self._activated_func = activated_func

        self._hotkey_mode = hotkey_mode
        
        self._thread_activation_toggle_event = threading.Event()
        self._thread_activation_toggle_event.clear()

    def _activation_handler(self):
        """
        Handle hotkey activation based on the hotkey mode.
        """

        if self._hotkey_mode == Hotkey_Modes.ONESHOT:
            self._activated_func()
        
        if self._hotkey_mode == Hotkey_Modes.TOGGLE:
            self._thread_activation_toggle_event.clear() if self._thread_activation_toggle_event.is_set() else self._thread_activation_toggle_event.set()

    def _activation_toggle(self):
        """
        If the hotkey mode is Hotkey_Modes.TOGGLE, stop and start the execution of a program depending on the state of the activation toggle event.
        """

        if self._hotkey_mode != Hotkey_Modes.TOGGLE:
            return
        
        while True:
            if self._thread_activation_toggle_event.is_set():
                self._activated_func()

    def run(self):
        """
        "Runs" the hotkey, as in starts listening for hotkey key combination presses.
        """
        
        thread_activation_handler = threading.Thread(target = self._activation_handler)
        thread_activation_toggle = threading.Thread(target = self._activation_toggle)
        hotkey = keyboard.HotKey(keyboard.HotKey.parse(self._key_combination), self._activation_handler)
        
        with keyboard.Listener(on_press = _for_canonical(hotkey.press), on_release = _for_canonical(hotkey.release)) as listener:
            listener.wait()
            logging_utils.logpr(f"Hotkey {self._key_combination} ready to run.")
            thread_activation_toggle.start()
            listener.join()
