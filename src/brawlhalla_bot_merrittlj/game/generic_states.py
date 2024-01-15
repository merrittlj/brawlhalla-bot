from __future__ import annotations
from abc import ABC, abstractmethod
import pyautogui, time

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils

from brawlhalla_bot_merrittlj.game import brawlhalla_bot
from brawlhalla_bot_merrittlj.game import ffa_bot
from brawlhalla_bot_merrittlj.game import ffa_states
from brawlhalla_bot_merrittlj.game import custom_game_bot
from brawlhalla_bot_merrittlj.game import custom_game_states

# "Generic" states that remain the same throughout the game/game modes.

class Legend_Selection(brawlhalla_bot.Game_State):
    def __str__(self):
        return "Legend Selection"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(129, 28, (162, 138, 120)) and pyautogui.pixelMatchesColor(130, 33, (166, 156, 143))  # Checks two brown pixels on the far-left of the top game UI.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(496, 20, (161, 126, 113)) and pyautogui.pixelMatchesColor(509, 9, (193, 173, 146))  # Checks two brown pixels on the far-left of the top game UI.

    def monitor(self) -> None:
        if isinstance(self.bot, ffa_bot.FFA_Bot):
            if ffa_states.Initial_Active_Match.matched_state(self.bot.resolution):
                logging_utils.logpr("Pixels scouted for the initial active match.")
                self.bot.state = ffa_states.Initial_Active_Match

        elif isinstance(self.bot, custom_game_bot.Custom_Game_Bot):
            if custom_game_states.Initial_Active_Match.matched_state(self.bot.resolution):
                logging_utils.logpr("Pixels scouted for the initial active match.")
                self.bot.state = custom_game_states.Initial_Active_Match

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("Selecting legend inputs.")
        logging_utils.logpr(f"Pressing \'{self.bot.input_keys.get('input_key_light_attack')}\' key every 0.5 seconds 3 times.  -- Menu selection")
        pyautogui.press(self.bot.input_keys.get('input_key_light_attack'), presses = 3, interval = 0.5)
            
class Pause(brawlhalla_bot.Game_State):
    def __str__(self):
        return "Pause"
    def matched_state(resolution) -> bool:    
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(391, 331, (0, 0, 51)) and pyautogui.pixelMatchesColor(382, 71, (223, 223, 3))  # Checks dark blue pause screen background pixel and yellow highlight on selected button.
            
            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(693, 606, (0, 0, 51)) and pyautogui.pixelMatchesColor(733, 200, (255, 255, 0))  # Checks dark blue pause screen background pixel and yellow highlight on selected button.
    
    def monitor(self) -> None:
        if Rejoin.matched_state(self.bot.resolution):
            logging_utils.logpr("Pixels scouted for rejoin screen.")
            self.bot.state = Rejoin

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("Running pause screen inputs.")

        logging_utils.logpr(f"Pressing \'{self.bot.input_keys.get('input_key_up')}\' key.    -- Menu up")
        pyautogui.press(self.bot.input_keys.get('input_key_up'))
        
        logging_utils.logpr("Sleeping inputs for 0.5 seconds.")
        time.sleep(0.5)
        
        logging_utils.logpr(f"Pressing {self.bot.input_keys.get('input_key_light_attack')} key.    -- Menu selection")
        pyautogui.press(self.bot.input_keys.get('input_key_light_attack'))

class Rejoin(brawlhalla_bot.Game_State):
    def __str__(self):
        return "Rejoin"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(296, 236, (0, 0, 51)) and pyautogui.pixelMatchesColor(416, 209, (56, 55, 62))  # Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.

            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(955, 491, (0, 0, 51)) and pyautogui.pixelMatchesColor(1264, 495, (56, 55, 62))  # Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.
    
    def monitor(self) -> None:
        if isinstance(self.bot, ffa_bot.FFA_Bot):
            if ffa_states.Final_Active_Match.matched_state(self.bot.resolution):
                logging_utils.logpr("Pixels scouted for the final active match.")
                self.bot.state = ffa_states.Final_Active_Match

        elif isinstance(self.bot, custom_game_bot.Custom_Game_Bot):
            if custom_game_states.Final_Active_Match.matched_state(self.bot.resolution):
                logging_utils.logpr("Pixels scouted for the final active match.")
                self.bot.state = custom_game_states.Final_Active_Match

    def inputs(self) -> None:
        if self.actions_ran == True:
            return
        
        self.actions_ran = True
        
        logging_utils.logpr("Running rejoin screen inputs.")

        logging_utils.logpr("Sleeping inputs for 6 seconds.")
        time.sleep(6)
                
        logging_utils.logpr(f"Pressing \'{self.bot.input_keys.get('input_key_light_attack')}\' key.  -- Menu selection")
        pyautogui.press(self.bot.input_keys.get('input_key_light_attack'))

class Game_Over(brawlhalla_bot.Game_State):
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
        if Legend_Selection.matched_state(self.bot.resolution):
            logging_utils.logpr("Pixels scouted for the legend selection.")
            self.bot.state = Legend_Selection

    def inputs(self) -> None:
        if self.actions_ran == True:
            # Will continuously press menu selection if this function is repeatedly called(as it should be) until state is changed to the next state(legend selection).
            logging_utils.logpr(f"Pressing {self.bot.input_keys.get('input_key_light_attack')} key.  -- Menu selection")
            pyautogui.press(self.bot.input_keys.get('input_key_light_attack'))
                    
            logging_utils.logpr("Sleeping inputs for 1 second.")
            time.sleep(1)
        
        self.actions_ran = True
        
        logging_utils.logpr("Running game over screen inputs.")

class Lost_Connection(brawlhalla_bot.Game_State):
    def __str__(self):
        return "Lost Connection"
    
    def matched_state(resolution) -> bool:
        match resolution:
            case pyautogui.Size(width = 600, height = 450):
                return pyautogui.pixelMatchesColor(223, 166, (0, 0, 51)) and pyautogui.pixelMatchesColor(285, 171, (254, 222, 1))  # Checks yellow pixel on coin symbol and background pixel on default avatar.

            case pyautogui.Size(width = 1920, height = 1080):
                return pyautogui.pixelMatchesColor(855, 336, (0, 0, 51)) and pyautogui.pixelMatchesColor(915, 408, (240, 209, 1))  # Checks yellow pixel on coin symbol and background pixel on default avatar.

    def self_monitor(self) -> None:
        if Lost_Connection.matched_state(self.bot.resolution):
            logging_utils.logpr("Pixels scouted for the lost connection screen.")
            self.bot.state = Lost_Connection
    
    def monitor(self) -> None:
        if Legend_Selection.matched_state(self.bot.resolution):
            logging_utils.logpr("Pixels scouted for the legend selection.")
            self.bot.state = Legend_Selection

    def inputs(self) -> None:
        if self.actions_ran == True:
            # Will continuously press menu selection if this function is repeatedly called(as it should be) until state is changed to the next state(legend selection).
            logging_utils.logpr(f"Pressing {self.bot.input_keys.get('input_key_light_attack')} key.  -- Menu selection")
            pyautogui.press(self.bot.input_keys.get('input_key_light_attack'))
                    
            logging_utils.logpr("Sleeping inputs for 2 seconds.")
            time.sleep(2)
        
        self.actions_ran = True
        
        logging_utils.logpr("Running game over screen inputs.")

        logging_utils.logpr(f"Pressing {self.bot.input_keys.get('input_key_light_attack')} key.    -- Menu selection")
        pyautogui.press(self.bot.input_keys.get('input_key_light_attack'))  # Return from lost connection screen to main menu.
