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
                # return pyautogui.pixelMatchesColor(312, 169, (255, 208, 101)) and pyautogui.pixelMatchesColor(304, 186, (255, 179, 88))  # Checks two pixels in 1 second number during countdown. More consistent that relying on in-game timers with low resolution.
                return pyautogui.pixelMatchesColor(405, 29, (253, 253, 253)) and pyautogui.pixelMatchesColor(407, 24, (221, 221, 221))  # In place due to the final active match state. If the previous checks are used, we will have to find something different for the final active match state anyways.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(1392, 69, (255, 255, 255)) and pyautogui.pixelMatchesColor(1396, 79, (255, 255, 255))  # In place due to the final active match state. If the previous checks are used, we will have to find something different for the final active match state anyways.
    
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
