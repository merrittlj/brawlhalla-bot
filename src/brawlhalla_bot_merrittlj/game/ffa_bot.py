import pyautogui, time

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils
from brawlhalla_bot_merrittlj.util import stoppable_thread

from brawlhalla_bot_merrittlj.game import brawlhalla_bot
from brawlhalla_bot_merrittlj.game import ffa_states
from brawlhalla_bot_merrittlj.game import generic_states


class FFA_Bot(brawlhalla_bot.Game_Bot):
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
            logging_utils.logpr(f"Running automatic-FFA in {str(5 - i)} seconds.")
            time.sleep(1)

        print("\n")
        self.program_running = True

        self._thread_state_monitor.start()
        self._thread_state_inputs.start()

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
        logging_utils.logpr(f"Current automatic-FFA running status: {self.program_running}")

        if not self.program_running:
            self.state = self._initial_state
            
            self._thread_state_monitor.stop()
            self._thread_state_inputs.stop()

            self._thread_state_monitor = stoppable_thread.StoppableThread(target = self._state_monitor)
            self._thread_state_inputs = stoppable_thread.StoppableThread(target = self._state_inputs)
            self._thread_state_monitor.start()
            self._theard_state_inputs.start()

    def print_state(self):
        logging_utils.logpr(f"Current automatic-FFA state: {type(state).__name__}.")
