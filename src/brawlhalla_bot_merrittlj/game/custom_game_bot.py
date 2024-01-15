import pyautogui, time

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils
from brawlhalla_bot_merrittlj.util import stoppable_thread

from brawlhalla_bot_merrittlj.game import brawlhalla_bot
from brawlhalla_bot_merrittlj.game import custom_game_states
from brawlhalla_bot_merrittlj.game import generic_states


class Custom_Game_Bot(brawlhalla_bot.Game_Bot):
    def __init__(self, state: brawlhalla_bot.Game_State, input_keys) -> None:
        self.state = state
        self._initial_state = self.state
        self.input_keys = input_keys
        self._resolution = pyautogui.size()
        self.program_running = False

        self._lost_connection_state = generic_states.Lost_Connection()
        self._lost_connection_state.bot = self
        self._thread_state_monitor = stoppable_thread.StoppableThread(target = self._state_monitor)
        self._thread_state_inputs = stoppable_thread.StoppableThread(target = self._state_inputs)

    def launch(self):
        for i in range(0, 5):
            logging_utils.logpr(f"Running custom-game bot in {str(5 - i)} seconds.")
            time.sleep(1)

        print("\n")
        self.program_running = True

        self.configure_lobby()

        self._thread_state_monitor.start()
        self._thread_state_inputs.start()

    def configure_lobby(self):
        logging_utils.logpr("Running legend selection inputs.")
        logging_utils.logpr("Setting up custom game lobby inputs.")


        # Open match settings.
        pyautogui.press(self.input_keys.get('input_key_heavy_attack'))
        time.sleep(0.5)

        # Change to timed mode.
        pyautogui.press(self.input_keys.get('input_key_right'))
        time.sleep(0.5)

        # Navigate to match length.
        pyautogui.press(self.input_keys.get('input_key_down'), presses = 2, interval = 0.5)
        time.sleep(0.5)

        # Change match length to 15 minutes.
        pyautogui.press(self.input_keys.get('input_key_left'), presses = 3, interval = 0.5)
        time.sleep(0.5)

        # Navigate to player count.
        pyautogui.press(self.input_keys.get('input_key_down'), presses = 7, interval = 0.5)
        time.sleep(0.5)

        # Change player count to 2.
        pyautogui.press(self.input_keys.get('input_key_left'), presses = 2, interval = 0.5)
        time.sleep(0.5)

        # Navigate to lobby settings.
        pyautogui.press(']')
        time.sleep(0.5)

        # Navigate to map selection.
        pyautogui.press(self.input_keys.get('input_key_down'), presses = 6, interval = 0.5)
        time.sleep(0.5)

        # Change map selection to random maps.
        pyautogui.press(self.input_keys.get('input_key_left'))
        time.sleep(0.5)

        # Navigate to handicaps.
        pyautogui.press(self.input_keys.get('input_key_down'), presses = 2, interval = 0.5)
        time.sleep(0.5)

        # Enable handicaps.
        pyautogui.press(self.input_keys.get('input_key_left'))
        time.sleep(0.5)

        # Navigate back to start.
        pyautogui.press(self.input_keys.get('input_key_up'), presses = 9, interval = 0.5)
        time.sleep(0.5)

        # Confirm changes.
        pyautogui.press(self.input_keys.get('input_key_light_attack'))
        time.sleep(0.5)

        # Go to party settings.
        pyautogui.press(self.input_keys.get('input_key_throw'))
        time.sleep(0.5)

        # Add bot and select its configuration.
        pyautogui.press(self.input_keys.get('input_key_light_attack'), presses = 2, interval = 0.5)
        time.sleep(0.5)

        # Change bot damage done to 50%.
        pyautogui.press(self.input_keys.get('input_key_left'), presses = 5, interval = 0.5)
        time.sleep(0.5)

        # Navigate to bot damage taken.
        pyautogui.press(self.input_keys.get('input_key_down'))
        time.sleep(0.5)

        # Change bot damage taken to 300%.
        pyautogui.press(self.input_keys.get('input_key_left'), presses = 6, interval = 0.5)
        time.sleep(0.5)

        # Navigate to bot difficulty.
        pyautogui.press(self.input_keys.get('input_key_down'), presses = 2, interval = 0.5)
        time.sleep(0.5)

        # Change bot difficulty to easy.
        pyautogui.press(self.input_keys.get('input_key_left'))
        time.sleep(0.5)

        # Confirm bot changes.
        pyautogui.press(self.input_keys.get('input_key_light_attack'))
        time.sleep(0.5)

        # Navigate to player.
        pyautogui.press(self.input_keys.get('input_key_up'))
        time.sleep(0.5)

        # Select player.
        pyautogui.press(self.input_keys.get('input_key_light_attack'))
        time.sleep(0.5)

        # Change player damage done to 300%.
        pyautogui.press(self.input_keys.get('input_key_left'), presses = 6, interval = 0.5)
        time.sleep(0.5)

        # Navigate to player damage taken.
        pyautogui.press(self.input_keys.get('input_key_down'))
        time.sleep(0.5)

        # Change player damage taken to 50%.
        pyautogui.press(self.input_keys.get('input_key_left'), presses = 5, interval = 0.5)
        time.sleep(0.5)

        # Confirm player settings.
        pyautogui.press(self.input_keys.get('input_key_light_attack'))
        time.sleep(0.5)

        # Exit party settings.
        pyautogui.press(self.input_keys.get('input_key_throw'))
        time.sleep(0.5)

    def _state_monitor(self):
        while not self._thread_state_monitor.stopped():
            self.state.monitor()
            if not isinstance(self.state, generic_states.Lost_Connection):
                self._lost_connection_state.self_monitor()

    def _state_inputs(self):
        while not self._thread_state_inputs.stopped():
            self.state.inputs()

    def program_running(self, program_running: bool):
        self._program_running = program_running
        
        print("\n")
        logging_utils.logpr(f"Current custom-game bot running status: {self.program_running}")

        if not self.program_running:
            self.state = self._initial_state
            
            self._thread_state_monitor.stop()
            self._thread_state_inputs.stop()

            self._thread_state_monitor = stoppable_thread.StoppableThread(target = self._state_monitor)
            self._thread_state_inputs = stoppable_thread.StoppableThread(target = self._state_inputs)
            self._thread_state_monitor.start()
            self._theard_state_inputs.start()

    def print_state(self):
        logging_utils.logpr(f"Current custom-game bot state: {type(state).__name__}.")
