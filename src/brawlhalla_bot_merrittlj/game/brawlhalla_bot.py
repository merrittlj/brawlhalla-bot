#!/usr/bin/env python3

import time, random, pyautogui, sys, threading

# "Local" imports
from brawlhalla_bot_merrittlj.util import logging_utils

location_states = ["Legend selection", "Active match", "Pause screen", "Rejoin screen", "Active match", "Game Over", "Lost connection"]

# State indexes
LEGEND_SELECTION = 0
FIRST_ACTIVE_MATCH = 1
PAUSE_SCREEN = 2
REJOIN_SCREEN = 3
SECOND_ACTIVE_MATCH = 4
GAME_OVER_SCREEN = 5
LOST_CONNECTION_SCREEN = 6  # Special state, not sequentially activated.


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
    def __init__(self, input_key_dict):
        self._input_key_dict = input_key_dict
        
        self._program_running = False

        self._state_index = 0
        self._state_action_ran = False

    def program_toggle(self):
        """
        Toggle the execution of the bot program on and off(usually called from a hotkey).
        """
        
        self._program_running = not self._program_running
        print("\n")
        logging_utils.logpr(f"FFA Bot running status: {self._program_running}\n")
        
        if (self._program_running == True):
            for i in range(0, 5):
                logging_utils.logpr(f"Running automatic-FFA in {str(5 - i)} seconds.")
                time.sleep(1)                        

            print("\n")
            
            thread_ffa_scout = threading.Thread(target = self._ffa_scout)
            thread_ffa_inputs = threading.Thread(target = self._ffa_inputs)

            thread_ffa_scout.start()
            thread_ffa_inputs.start()
        
    def _ffa_scout(self):
        """
        "Scout"/analyze the screen for pixels that match varying states.
        """
        
        global location_states
                
        while True:
            # Matching pixels on a 600x450 window(X nested server).
            if pyautogui.pixelMatchesColor(135, 38, (168, 127, 105)) and pyautogui.pixelMatchesColor(128, 40, (166, 124, 102)):  # We are in the legend selection. Checks two brown pixels on the far left of the top game-UI.
                logging_utils.logpr("Pixels matched for legend selection.")
                if self._state_index == GAME_OVER_SCREEN:
                    self._state_index = LEGEND_SELECTION
                    self._state_action_ran = False
                elif self._state_index != LEGEND_SELECTION and self._state_index != LOST_CONNECTION_SCREEN:  # Legend selection may appear when attempting to restore connection.
                    logging_utils.logpr(f"Incorrect state {location_states[self._state_index]} when state should be legend selection or game over screen. Exitting.")
                    sys.exit()

            elif pyautogui.pixelMatchesColor(407, 48, (252, 252, 252)) and pyautogui.pixelMatchesColor(410, 44, (235, 235, 235)):  # We are in an active match. Checks two white pixels in the game timer.
                logging_utils.logpr("Pixels matched for an active match.")
                if self._state_index == LEGEND_SELECTION:
                    self._state_index = FIRST_ACTIVE_MATCH
                    self._state_action_ran = False
                elif self._state_index == REJOIN_SCREEN:
                    self._state_index = SECOND_ACTIVE_MATCH
                    self._state_action_ran = False
                elif self._state_index != FIRST_ACTIVE_MATCH and self._state_index != SECOND_ACTIVE_MATCH and self._state_index != PAUSE_SCREEN:  # Pause screen can match active match pixels.
                    logging_utils.logpr(f"Incorrect state {location_states[self._state_index]} when state should be legend selection, rejoin screen, first active match, pause screen, or second active match. Exitting.")
                    sys.exit()

            elif pyautogui.pixelMatchesColor(403, 387, (0, 0, 51)) and pyautogui.pixelMatchesColor(345, 63, (96, 152, 171)):  # We are in the pause screen. Checks dark blue pause screen background pixel and options text cyan color.
                logging_utils.logpr("Pixels matched for the pause screen.")
                if self._state_index == FIRST_ACTIVE_MATCH:
                    self._state_index = PAUSE_SCREEN
                    self._state_action_ran = False
                elif self._state_index != PAUSE_SCREEN:
                    logging_utils.logpr(f"Incorrect state {location_states[self._state_index]} when state should be first active match or pause screen. Exitting.")
                    sys.exit()

            elif pyautogui.pixelMatchesColor(418, 219, (56, 55, 62)) and pyautogui.pixelMatchesColor(450, 209, (0, 0, 51)):  # We are in the rejoin screen. Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.
                logging_utils.logpr("Pixels matched for the rejoin screen.")
                if self._state_index == PAUSE_SCREEN:
                    self._state_index = REJOIN_SCREEN
                    self._state_action_ran = False
                elif self._state_index == LOST_CONNECTION_SCREEN:
                    logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_dodge')} key.  -- Menu back")
                    pyautogui.press(self._input_key_dict.get('input_key_dodge'))
                elif self._state_index != REJOIN_SCREEN:
                    logging_utils.logpr(f"Incorrect state {location_states[self._state_index]} when state should be pause screen or rejoin screen. Exitting.")
                    sys.exit()

            elif pyautogui.pixelMatchesColor(574, 49, (219, 207, 82)) and pyautogui.pixelMatchesColor(462, 44, (52, 42, 128)):  # We are in the game over screen. Checks yellow pixel on coin symbol and background pixel on default avatar.
                logging_utils.logpr("Pixels matched for the game over screen.")
                if self._state_index == SECOND_ACTIVE_MATCH:  # Was in an active match, now in the game over screen.
                    self._state_index = GAME_OVER_SCREEN
                    self._state_action_ran = False
                elif self._state_index != GAME_OVER_SCREEN and self._state_index != REJOIN_SCREEN and self._state_index != LOST_CONNECTION_SCREEN:  # Game over pixels can sometimes appear after the rejoin screen, which we want to ignore.
                    logging_utils.logpr(f"Incorrect state {location_states[self._state_index]} when state should be second active match or game over screen. Exitting.")
                    sys.exit()

            elif pyautogui.pixelMatchesColor(310, 187, (241, 210, 1)) and pyautogui.pixelMatchesColor(377, 262, (0, 0, 51)):  # We are in the lost connection screen. Checks yellow pixel on warning symbol and dark blue background pixel on warning UI.
                logging_utils.logpr("Pixels matched for the lost connection screen.")
                self._state_index = LOST_CONNECTION_SCREEN
                self._state_action_ran = False


            if self._program_running == False:
                logging_utils.logpr("automatic-FFA scout shutting down.")
                return

            logging_utils.logpr(f"Current automatic-FFA state: {location_states[self._state_index]}, internal number: {str(self._state_index)}.")
            if self._state_index == LOST_CONNECTION_SCREEN:  # Debugging.
                pix1 = pyautogui.pixel(466, 51)
                pix2 = pyautogui.pixel(497, 45)
                logging_utils.logpr(f"POS1(466, 51): ({pix1[0]}, {pix1[1]}, {pix1[2]}) POS2(497, 45): ({pix2[0]}, {pix2[1]}, {pix2[2]})")

            time.sleep(1)

    def _ffa_inputs(self):
        """
        Input the correct keys depending on the automatic-FFA state.
        """
        
        global location_states
        
        logging_utils.logpr("Running automatic-FFA inputs.")
        
        while True:
            if self._program_running == False:
                logging_utils.logpr("automatic-FFA inputs shutting down.")
                return
            
            if self._state_action_ran:
                continue
            
            elif self._state_index == LEGEND_SELECTION:
                self._state_action_ran = True
                logging_utils.logpr("Running legend selection actions.")

                logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_light_attack')} key every 0.5 seconds 3 times.  -- Menu selection")
                pyautogui.press(self._input_key_dict.get('input_key_light_attack'), presses = 3, interval = 0.5)
            
            elif self._state_index == FIRST_ACTIVE_MATCH:
                self._state_action_ran = True
                logging_utils.logpr("Running initial active game actions.")
                
                logging_utils.logpr("Sleeping inputs for 5 seconds.")
                time.sleep(5)
                
                while self._state_index != PAUSE_SCREEN:
                    logging_utils.logpr("Pressing ESC key.  -- Pause menu")
                    pyautogui.press('esc')
                    logging_utils.logpr("Sleeping inputs for 1 second.")
                    time.sleep(1)
            
            elif self._state_index == PAUSE_SCREEN:  # Variable amount of ESC key presses.
                self._state_action_ran = True
                logging_utils.logpr("Running pause screen actions.")
                
                logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_aim_up')} key.    -- Menu up")
                pyautogui.press(self._input_key_dict.get('input_key_aim_up'))
                
                logging_utils.logpr("Sleeping inputs for 0.5 seconds.")
                time.sleep(0.5)
                
                logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_light_attack')} key.    -- Menu selection")
                pyautogui.press(self._input_key_dict.get('input_key_light_attack'))
                
            elif self._state_index == REJOIN_SCREEN:
                self._state_action_ran = True
                logging_utils.logpr("Running rejoin screen actions.")
                
                logging_utils.logpr("Sleeping inputs for 6 seconds.")
                time.sleep(6)
                
                logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_light_attack')} key every 0.1 seconds 2 times.  -- Menu selection")
                pyautogui.press(self._input_key_dict.get('input_key_light_attack'), presses = 2, interval = 0.05)
                
            elif self._state_index == GAME_OVER_SCREEN:  # Variable amount of menus to go through.
                self._state_action_ran = True
                logging_utils.logpr("Running game over actions.")
                
                while self._state_index == GAME_OVER_SCREEN:
                    logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_light_attack')} key.  -- Menu selection")
                    pyautogui.press(self._input_key_dict.get('input_key_light_attack'))
                    
                    logging_utils.logpr("Sleeping inputs for 1 second.")
                    time.sleep(1)
                    
            elif self._state_index == LOST_CONNECTION_SCREEN:  # Attempts to restore connection periodically.
                self._state_action_ran = True
                logging_utils.logpr("Running lost connection screen actions.")
                
                logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_light_attack')} key.    -- Menu selection")
                pyautogui.press(self._input_key_dict.get('input_key_light_attack'))  # Return from lost connection screen to main menu.
                # Checks that the "offline" text is still present.
                while pyautogui.pixelMatchesColor(466, 51, (34, 62, 86)) and pyautogui.pixelMatchesColor(497, 45, (14, 19, 50)):
                    logging_utils.logpr(f"Pressing {self._input_key_dict.get('input_key_light_attack')} key.  -- Menu selection")
                    pyautogui.press(self._input_key_dict.get('input_key_light_attack'))
                    logging_utils.logpr("Sleeping inputs for 2 seconds.")
                    time.sleep(2)
