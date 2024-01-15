#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils


class Game_Bot(ABC):
    _inital_state = None
    _state = None
    _input_keys = None
    _resolution = None
    _program_running = False

    
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: brawlhalla_bot.Game_State):
        logging_utils.logpr(f"Context: Transitioning to {str(state())}.")
        
        self._state = state()
        self._state.bot = self

    @property
    def input_keys(self) -> dict[str, int]:
        return self._input_keys

    @input_keys.setter
    def input_keys(self, input_keys: dict[str, int]) -> None:
        self._input_keys = input_keys

    @property
    def resolution(self):
        return self._resolution

    @property
    def program_running(self) -> bool:
        return self._program_running

    @program_running.setter
    @abstractmethod
    def program_running(self, program_running: bool) -> None:
        self._program_running = program_running

    def program_toggle(self):
        """
        Toggle the execution of the bot program on and off(usually called from a hotkey).
        """
        
        if self.program_running:
            self.program_running(False)
        else:
            self.launch()

    @abstractmethod
    def launch(self) -> None:
        raise NotImplementedError

class Game_State(ABC):
    _bot = None
    _actions_ran = False

    @abstractmethod
    def __str__(self):
        raise NotImplementedError
    
    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot) -> None:
        self._bot = bot

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
