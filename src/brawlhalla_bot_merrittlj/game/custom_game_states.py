from __future__ import annotations
from abc import ABC, abstractmethod
import pyautogui, time

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils

from brawlhalla_bot_merrittlj.game import brawlhalla_bot
from brawlhalla_bot_merrittlj.game import generic_states


class Initial_Active_Match(brawlhalla_bot.Game_State):
    def __str__(self):
        return "Initial Active Match"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return (pyautogui.pixel(473, 27)[0] > 240) and pyautogui.pixelMatchesColor(473, 26, (251, 251, 251))  # In place due to the final active match state.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(1578, 70, (255, 255, 255)) and pyautogui.pixelMatchesColor(1576, 78, (254, 254, 254))  # In place due to the final active match state.
    
    def monitor(self) -> None:
        if generic_states.Pause.matched_state(self.bot.resolution):
            logging_utils.logpr("Pixels scouted for the pause screen.")
            self.bot.state = generic_states.Pause

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

class Final_Active_Match(brawlhalla_bot.Game_State):
    def __str__(self):
        return "Final Active Match"
    
    def matched_state(resolution) -> bool:
        return Initial_Active_Match.matched_state(resolution)
    
    def monitor(self) -> None:
        if generic_states.Game_Over.matched_state(self.bot.resolution):
            logging_utils.logpr("Pixels scouted for the game over screen.")
            self.bot.state = generic_states.Game_Over

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("No inputs for final active match.")
