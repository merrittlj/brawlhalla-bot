#!/usr/bin/env python3

from __future__ import annotations
import time, random, pyautogui, sys
from enum import Enum
from abc import ABC, abstractmethod

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils
from brawlhalla_bot_merrittlj.util import stoppable_thread


def run_random_inputs():  # May have use in custom games, but is not used in FFA due to inefficiency.
    """
    Inputs random keys, may have use in custom games; however, this is not used in FFA due to inefficiency. Code is not updated for new input system and will error.
    """
    
    while True:
        if bot_running_event.is_set():
            rand_input, input_description = random.choice(list(input_dictionary.items()))
            rand_time = random.randint(5, 25) / 100  # Generate times 0.05 .. 0.25 seconds.

            logging_utils.logpr(f"Inputting key: \'{rand_input}\' for {str(rand_time)} seconds.{' ' * (4 - len(str(rand_time)))}-- {input_description}")
                
            pyautogui.keyDown(rand_input)
            time.sleep(rand_time)
            pyautogui.keyUp(rand_input)

def position_testing():
    """
    Print the position and color of the pixel under the mouse every second. Used for debugging.
    """
    
    while True:
        pos = pyautogui.position()
        pix = pyautogui.pixel(pos[0], pos[1])
        logging_utils.logpr(f"POS: ({str(pos[0])}, {str(pos[1])}), RGB: ({str(pix[0])}, {str(pix[1])}, {str(pix[2])})")
        time.sleep(1)

class FFA_Bot:
    def __init__(self, state: State, input_key_dict) -> None:
        self.set_state(state)
        self._initial_state = state
        self._input_key_dict = input_key_dict
        self._resolution = pyautogui.size()
        self._lost_connection_state = Lost_Connection()
        self._lost_connection_state.ffa_bot = self
        
        self._program_running = False
        
        self._thread_state_monitor = stoppable_thread.StoppableThread(target = self._state_monitor)
        self._thread_state_inputs = stoppable_thread.StoppableThread(target = self._state_inputs)

    def launch(self):
        for i in range(0, 5):
            logging_utils.logpr(f"Running automatic-FFA in {str(5 - i)} seconds.")
            time.sleep(1)

        print("\n")
        self.set_program_running(True)

        self._thread_state_monitor.start()
        self._thread_state_inputs.start()

    def set_state(self, state: State):
        logging_utils.logpr(f"Context: Transitioning to {str(state())}.")
        
        self._state = state()
        self._state.ffa_bot = self

    def _state_monitor(self):
        while not self._thread_state_monitor.stopped():
            self._state.monitor()
            if not isinstance(self._state, Lost_Connection):
                self._lost_connection_state.self_monitor()

    def _state_inputs(self):
        while not self._thread_state_inputs.stopped():
            self._state.inputs()

    def get_resolution(self):
        return self._resolution

    def set_program_running(self, program_running):
        self._program_running = program_running
        
        print("\n")
        logging_utils.logpr(f"Current automatic-FFA running status: {self._program_running}")

        if not self._program_running:
            self._state = self._initial_state
            
            self._thread_state_monitor.stop()
            self._thread_state_inputs.stop()

            self._thread_state_monitor = stoppable_thread.StoppableThread(target = self._state_monitor)
            self._thread_state_inputs = stoppable_thread.StoppableThread(target = self._state_inputs)
            self._thread_state_monitor.start()
            self._theard_state_inputs.start()

    def present_state(self):
        logging_utils.logpr(f"Current automatic-FFA state: {type(state).__name__}.")

    def input_key_lookup(self, input_key):
        return self._input_key_dict.get(input_key)

    
    def program_toggle(self):
        """
        Toggle the execution of the bot program on and off(usually called from a hotkey).
        """
        
        if self._program_running:
            self.set_program_running(False)
        else:
            self.launch()

class FFA_State(ABC):
    _ffa_bot = None
    _actions_ran = False

    @abstractmethod
    def __str__(self):
        raise NotImplementedError
    
    @property
    def ffa_bot(self) -> FFA_Bot:
        return self._ffa_bot

    @ffa_bot.setter
    def ffa_bot(self, ffa_bot: FFA_Bot) -> None:
        self._ffa_bot = ffa_bot

    @property
    def actions_ran(self) -> bool:
        return self._actions_ran

    @actions_ran.setter
    def actions_ran(self, actions_ran: bool) -> None:
        self._actions_ran = actions_ran

        
    def matched_state(resolution) -> bool:
        """
        Returns True/False if this state is "matched" or not(usually if pixels for the state are present on the passed resolution screen).
        """
        
        raise NotImplementedError
        
    @abstractmethod
    def monitor(self) -> None:
        """
        Check if we should transition the bot to the next state(uses _matched_state).
        """
        
        raise NotImplementedError

    @abstractmethod
    def inputs(self) -> None:
        """
        Run the inputs respective to the current state.
        """
        
        raise NotImplementedError

class Legend_Selection(FFA_State):
    def __str__(self):
        return "Legend Selection"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(129, 28, (162, 138, 120)) and pyautogui.pixelMatchesColor(130, 33, (166, 156, 143))  # Checks two brown pixels on the far-left of the top game UI.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(496, 20, (161, 126, 113)) and pyautogui.pixelMatchesColor(509, 9, (193, 173, 146))  # Checks two brown pixels on the far-left of the top game UI.
    
    def monitor(self) -> None:
        if Initial_Active_Match.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the initial active match.")
            self.ffa_bot.set_state(Initial_Active_Match)

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("Running legend selection inputs.")

        logging_utils.logpr(f"Pressing \'{self.ffa_bot.input_key_lookup('input_key_light_attack')}\' key every 0.5 seconds 3 times.  -- Menu selection")
        pyautogui.press(self.ffa_bot.input_key_lookup('input_key_light_attack'), presses = 3, interval = 0.5)

class Initial_Active_Match(FFA_State):
    def __str__(self):
        return "Initial Active Match"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                # return pyautogui.pixelMatchesColor(312, 169, (255, 208, 101)) and pyautogui.pixelMatchesColor(304, 186, (255, 179, 88))  # Checks two pixels in 1 second number during countdown. More consistent that relying on in-game timers with low resolution.
                return pyautogui.pixelMatchesColor(405, 29, (253, 253, 253)) and pyautogui.pixelMatchesColor(407, 24, (221, 221, 221))  # In place due to the final active match state. If the previous checks are used, we will have to find something different for the final active match state anyways.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(1392, 69, (255, 255, 255)) and pyautogui.pixelMatchesColor(1396, 79, (255, 255, 255))  # In place due to the final active match state. If the previous checks are used, we will have to find something different for the final active match state anyways.
    
    def monitor(self) -> None:
        if Pause.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the pause screen.")
            self.ffa_bot.set_state(Pause)

    def inputs(self) -> None:
        if self.actions_ran == True:
            # Will continuously press ESC if this function is repeatedly called(as it should be) until state is changed to the next state(pause screen).
            logging_utils.logpr("Pressing ESC key.  -- Pause menu")
            pyautogui.press('esc')
            logging_utils.logpr("Sleeping inputs for 1 second.")
            time.sleep(1)
        
        self.actions_ran = True
        
        logging_utils.logpr("Running active match inputs.")
        
        logging_utils.logpr("Sleeping inputs 5 seconds.")
        time.sleep(5)

class Pause(FFA_State):
    def __str__(self):
        return "Pause"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(391, 331, (0, 0, 51)) and pyautogui.pixelMatchesColor(382, 71, (223, 223, 3))  # Checks dark blue pause screen background pixel and yellow highlight on selected button.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(693, 606, (0, 0, 51)) and pyautogui.pixelMatchesColor(733, 200, (255, 255, 0))  # Checks dark blue pause screen background pixel and yellow highlight on selected button.
    
    def monitor(self) -> None:
        if Rejoin.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for rejoin screen.")
            self.ffa_bot.set_state(Rejoin)

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("Running pause screen inputs.")

        logging_utils.logpr(f"Pressing \'{self.ffa_bot.input_key_lookup('input_key_up')}\' key.    -- Menu up")
        pyautogui.press(self.ffa_bot.input_key_lookup('input_key_up'))
        
        logging_utils.logpr("Sleeping inputs for 0.5 seconds.")
        time.sleep(0.5)
        
        logging_utils.logpr(f"Pressing {self.ffa_bot.input_key_lookup('input_key_light_attack')} key.    -- Menu selection")
        pyautogui.press(self.ffa_bot.input_key_lookup('input_key_light_attack'))

class Rejoin(FFA_State):
    def __str__(self):
        return "Rejoin"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(296, 236, (0, 0, 51)) and pyautogui.pixelMatchesColor(416, 209, (56, 55, 62))  # Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.

            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(955, 491, (0, 0, 51)) and pyautogui.pixelMatchesColor(1264, 495, (56, 55, 62))  # Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.
    
    def monitor(self) -> None:
        if Final_Active_Match.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the final active match.")
            self.ffa_bot.set_state(Final_Active_Match)

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("Running rejoin screen inputs.")

        logging_utils.logpr("Sleeping inputs for 6 seconds.")
        time.sleep(6)
                
        logging_utils.logpr(f"Pressing \'{self.ffa_bot.input_key_lookup('input_key_light_attack')}\' key every 0.1 seconds 2 times.  -- Menu selection")
        pyautogui.press(self.ffa_bot.input_key_lookup('input_key_light_attack'), presses = 2, interval = 0.05)

class Final_Active_Match(FFA_State):
    def __str__(self):
        return "Final Active Match"
    
    def matched_state(resolution) -> bool:
        return Initial_Active_Match.matched_state(resolution)
    
    def monitor(self) -> None:
        if Game_Over.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the game over screen.")
            self.ffa_bot.set_state(Game_Over)

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("No inputs for final active match.")

class Game_Over(FFA_State):
    def __str__(self):
        return "Game Over"
    
    def matched_state(resolution) -> bool:
        # TODO: Maybe change this? Checks a pixel on the default avatar.
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(459, 38, (52, 42, 128)) and pyautogui.pixelMatchesColor(571, 39, (204, 166, 74))  # Checks yellow pixel on coin symbol and background pixel on default avatar.

            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(1539, 29, (52, 42, 128)) and pyautogui.pixelMatchesColor(1840, 35, (225, 208, 62))  # Checks yellow pixel on coin symbol and background pixel on default avatar.
                
    
    def monitor(self) -> None:
        if Legend_Selection.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the legend selection.")
            self.ffa_bot.set_state(Legend_Selection)

    def inputs(self) -> None:
        if self.actions_ran == True:
            # Will continuously press menu selection if this function is repeatedly called(as it should be) until state is changed to the next state(legend selection).
            logging_utils.logpr(f"Pressing {self.ffa_bot.input_key_lookup('input_key_light_attack')} key.  -- Menu selection")
            pyautogui.press(self.ffa_bot.input_key_lookup('input_key_light_attack'))
                    
            logging_utils.logpr("Sleeping inputs for 1 second.")
            time.sleep(1)
        
        self.actions_ran = True
        
        logging_utils.logpr("Running game over screen inputs.")

class Lost_Connection(FFA_State):
    def __str__(self):
        return "Lost Connection"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(223, 166, (0, 0, 51)) and pyautogui.pixelMatchesColor(285, 171, (254, 222, 1))  # Checks yellow pixel on coin symbol and background pixel on default avatar.

            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(855, 336, (0, 0, 51)) and pyautogui.pixelMatchesColor(915, 408, (240, 209, 1))  # Checks yellow pixel on coin symbol and background pixel on default avatar.

    def self_monitor(self) -> None:
        if Lost_Connection.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the lost connection screen.")
            self.ffa_bot.set_state(Lost_Connection)
    
    def monitor(self) -> None:
        if Legend_Selection.matched_state(self.ffa_bot.get_resolution()):
            logging_utils.logpr("Pixels scouted for the legend selection.")
            self.ffa_bot.set_state(Legend_Selection)

    def inputs(self) -> None:
        if self.actions_ran == True:
            # Will continuously press menu selection if this function is repeatedly called(as it should be) until state is changed to the next state(legend selection).
            logging_utils.logpr(f"Pressing {self.ffa_bot.input_key_lookup('input_key_light_attack')} key.  -- Menu selection")
            pyautogui.press(self.ffa_bot.input_key_lookup('input_key_light_attack'))
                    
            logging_utils.logpr("Sleeping inputs for 2 seconds.")
            time.sleep(2)
        
        self.actions_ran = True
        
        logging_utils.logpr("Running game over screen inputs.")

        logging_utils.logpr(f"Pressing {self.ffa_bot.input_key_lookup('input_key_light_attack')} key.    -- Menu selection")
        pyautogui.press(self.ffa_bot.input_key_lookup('input_key_light_attack'))  # Return from lost connection screen to main menu.
