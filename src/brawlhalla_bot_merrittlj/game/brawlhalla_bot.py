#!/usr/bin/env python3

import time, random, pyautogui, sys

# "Local" imports
# From util/
from brawlhalla_bot_merrittlj.util import logging_utils

bot_running = False

location_states = ["Legend selection", "Active match", "Pause screen", "Rejoin screen", "Active match", "Game Over", "Lost connection"]
state_index = 0
state_action_ran = False

# State indexes
LEGEND_SELECTION = 0
FIRST_ACTIVE_MATCH = 1
PAUSE_SCREEN = 2
REJOIN_SCREEN = 3
SECOND_ACTIVE_MATCH = 4
GAME_OVER_SCREEN = 5
LOST_CONNECTION_SCREEN = 6  # Special state, not sequentially activated.

input_description_dictionary = {  # Match input keys to descriptions
    INPUT_KEY_LEFT: "Move left",
    INPUT_KEY_RIGHT: "Move right",
    INPUT_KEY_AIM_UP: "Aim up",
    INPUT_KEY_DOWN: "Down",
    INPUT_KEY_JUMP: "Jump",

    INPUT_KEY_LIGHT_ATTACK: "Light attack",
    INPUT_KEY_HEAVY_ATTACK: "Heavy attack",
    INPUT_KEY_THROW: "Throw/pickup",
    INPUT_KEY_DODGE: "Dodge/dash",
}

bot_running_event = threading.Event()
listener = keyboard.Listener()

thread_one_scout = None 
thread_two_inputs = None

def toggle_hotkey_activated():
    logging_utils.logpr(f"\nToggle hotkey {toggle_key_combination} activated.")
    
    global bot_running
    bot_running = not bot_running
    if bot_running:            
        bot_running_event.set()

        logging_utils.logpr("Starting bot.\n")
    else:
        bot_running_event.clear()

        logging_utils.logpr("Stopping bot.\n")

def main():
    global thread_one_scout
    global thread_two_inputs
    
    thread_one_scout = threading.Thread(target = auto_ffa_scout)
    thread_two_inputs = threading.Thread(target = auto_ffa_inputs)
    # thread_three_testing = threading.Thread(target = position_testing)
    
    toggle_hotkey = keyboard.HotKey(keyboard.HotKey.parse(toggle_key_combination), toggle_hotkey_activated)
    with keyboard.Listener(
            on_press = for_canonical(toggle_hotkey.press),  # In this scenario, keys are translated cannonically before being passed into "hotkey.press".
            on_release = for_canonical(toggle_hotkey.release)
    ) as listener:
        listener.wait()
        logging_utils.logpr("Ready to run.")
        thread_one_scout.start()
        # thread_three_testing.start()
        listener.join()

def run_random_inputs():  # May have use in custom games, but is not used in FFA due to inefficiency.
    while True:
        if bot_running_event.is_set():
            rand_input, input_description = random.choice(list(input_dictionary.items()))
            rand_time = random.randint(5, 25) / 100  # Generate times 0.05 .. 0.25 seconds.

            logging_utils.logpr(f"Inputting key: \'{rand_input}\' for {str(rand_time)} seconds.{' ' * (4 - len(str(rand_time)))}-- {input_description}")
                
            pyautogui.keyDown(rand_input)
            time.sleep(rand_time)
            pyautogui.keyUp(rand_input)

def auto_ffa_scout():  # "Scouts" the screen for pixels to match a state.
    global location_states
    global state_index
    global state_action_ran
    global thread_two_inputs

    while True:
        if bot_running_event.is_set():
            for i in range(0, 5):
                logging_utils.logpr("Running auto-FFA in " + str(5 - i) + " seconds.")
                time.sleep(1)

            break
        
    logging_utils.logpr("\n")            
    thread_two_inputs.start()

    while True:
        # Matching pixels on a 600x450 window(X nested server).
        if pyautogui.pixelMatchesColor(135, 38, (168, 127, 105)) and pyautogui.pixelMatchesColor(128, 40, (166, 124, 102)):  # We are in the legend selection. Checks two brown pixels on the far left of the top game-UI.
            logging_utils.logpr("Pixels matched for legend selection.")
            if state_index == GAME_OVER_SCREEN:
                state_index = LEGEND_SELECTION
                state_action_ran = False
            elif state_index != LEGEND_SELECTION and state_index != LOST_CONNECTION_SCREEN:  # Legend selection may appear when attempting to restore connection.
                logging_utils.logpr("Incorrect state " + location_states[state_index] + " when state should be legend selection or game over screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(407, 48, (252, 252, 252)) and pyautogui.pixelMatchesColor(410, 44, (235, 235, 235)):  # We are in an active match. Checks two white pixels in the game timer.
            logging_utils.logpr("Pixels matched for an active match.")
            if state_index == LEGEND_SELECTION:
                state_index = FIRST_ACTIVE_MATCH
                state_action_ran = False
            elif state_index == REJOIN_SCREEN:
                state_index = SECOND_ACTIVE_MATCH
                state_action_ran = False
            elif state_index != FIRST_ACTIVE_MATCH and state_index != SECOND_ACTIVE_MATCH and state_index != PAUSE_SCREEN:  # Pause screen can match active match pixels.
                logging_utils.logpr("Incorrect state " + location_states[state_index] + " when state should be legend selection, rejoin screen, first active match, pause screen, or second active match. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(403, 387, (0, 0, 51)) and pyautogui.pixelMatchesColor(345, 63, (96, 152, 171)):  # We are in the pause screen. Checks dark blue pause screen background pixel and options text cyan color.
            logging_utils.logpr("Pixels matched for the pause screen.")
            if state_index == FIRST_ACTIVE_MATCH:
                state_index = PAUSE_SCREEN
                state_action_ran = False
            elif state_index != PAUSE_SCREEN:
                logging_utils.logpr("Incorrect state " + location_states[state_index] + " when state should be first active match or pause screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(418, 219, (56, 55, 62)) and pyautogui.pixelMatchesColor(450, 209, (0, 0, 51)):  # We are in the rejoin screen. Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.
            logging_utils.logpr("Pixels matched for the rejoin screen.")
            if state_index == PAUSE_SCREEN:
                state_index = REJOIN_SCREEN
                state_action_ran = False
            elif state_index == LOST_CONNECTION_SCREEN:
                logging_utils.logpr("Pressing " + INPUT_KEY_DODGE + " key.  -- Menu back")
                pyautogui.press(INPUT_KEY_DODGE)
            elif state_index != REJOIN_SCREEN:
                logging_utils.logpr("Incorrect state " + location_states[state_index] + " when state should be pause screen or rejoin screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(574, 49, (219, 207, 82)) and pyautogui.pixelMatchesColor(462, 44, (52, 42, 128)):  # We are in the game over screen. Checks yellow pixel on coin symbol and background pixel on default avatar.
            logging_utils.logpr("Pixels matched for the game over screen.")
            if state_index == SECOND_ACTIVE_MATCH:  # Was in an active match, now in the game over screen.
                state_index = GAME_OVER_SCREEN
                state_action_ran = False
            elif state_index != GAME_OVER_SCREEN and state_index != REJOIN_SCREEN and state_index != LOST_CONNECTION_SCREEN:  # Game over pixels can sometimes appear after the rejoin screen, which we want to ignore.
                logging_utils.logpr("Incorrect state " + location_states[state_index] + " when state should be second active match or game over screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(310, 187, (241, 210, 1)) and pyautogui.pixelMatchesColor(377, 262, (0, 0, 51)):  # We are in the lost connection screen. Checks yellow pixel on warning symbol and dark blue background pixel on warning UI.
            logging_utils.logpr("Pixels matched for the lost connection screen.")
            state_index = LOST_CONNECTION_SCREEN
            state_action_ran = False

        print (logging_header + "Current FFA state: " + location_states[state_index] + ", internal number: " + str(state_index) + ".")
        if state_index == LOST_CONNECTION_SCREEN:
            pix1 = pyautogui.pixel(466, 51)
            pix2 = pyautogui.pixel(497, 45)
            logging_utils.logpr("POS1(466, 51): (" + pix1[0] + ", " + pix1[1] + ", " + pix1[2] + ") POS2(497, 45): (" + pix2[0] + ", " + pix2[1] + ", " + pix2[2] + ")")
                
        time.sleep(1)

def auto_ffa_inputs():
    global location_states
    global state_index
    global state_action_ran
    
    logging_utils.logpr("Running auto-FFA inputs.")
    
    while True:
        if state_action_ran:
            continue
        
        elif state_index == LEGEND_SELECTION:
            state_action_ran = True
            logging_utils.logpr("Legend selection actions.")

            logging_utils.logpr("Pressing " + INPUT_KEY_LIGHT_ATTACK + " key every 0.5 seconds 3 times.  -- Menu selection")
            pyautogui.press(INPUT_KEY_LIGHT_ATTACK, presses = 3, interval = 0.5)
        
        elif state_index == FIRST_ACTIVE_MATCH:
            state_action_ran = True
            logging_utils.logpr("Initial active game actions.")

            logging_utils.logpr("Sleeping inputs for 5 seconds.")
            time.sleep(5)

            while state_index != PAUSE_SCREEN:
                logging_utils.logpr("Pressing ESC key.  -- Pause menu")
                pyautogui.press('esc')
                logging_utils.logpr("Sleeping inputs for 1 second.")
                time.sleep(1)

        elif state_index == PAUSE_SCREEN:  # Variable amount of ESC key presses.
            state_action_ran = True
            logging_utils.logpr("Pause screen actions.")

            logging_utils.logpr("Pressing " + INPUT_KEY_AIM_UP + " key.    -- Menu up")
            pyautogui.press(INPUT_KEY_AIM_UP)

            logging_utils.logpr("Sleeping inputs for 0.5 seconds.")
            time.sleep(0.5)

            logging_utils.logpr("Pressing " + INPUT_KEY_LIGHT_ATTACK + " key.    -- Menu selection")
            pyautogui.press(INPUT_KEY_LIGHT_ATTACK)

        elif state_index == REJOIN_SCREEN:
            state_action_ran = True
            logging_utils.logpr("Rejoin screen actions.")

            logging_utils.logpr("Sleeping inputs for 6 seconds.")
            time.sleep(6)

            logging_utils.logpr("Pressing " + INPUT_KEY_LIGHT_ATTACK + " key every 0.1 seconds 2 times.  -- Menu selection")
            pyautogui.press(INPUT_KEY_LIGHT_ATTACK, presses = 2, interval = 0.05)

        elif state_index == GAME_OVER_SCREEN:  # Variable amount of menus to go through.
            state_action_ran = True
            logging_utils.logpr("Game over actions.")

            while state_index == GAME_OVER_SCREEN:
                logging_utils.logpr("Pressing " + INPUT_KEY_LIGHT_ATTACK + " key.  -- Menu selection")
                pyautogui.press(INPUT_KEY_LIGHT_ATTACK)
                
                logging_utils.logpr("Sleeping inputs for 1 second.")
                time.sleep(1)

        elif state_index == LOST_CONNECTION_SCREEN:  # Attempts to restore connection periodically.
            state_action_ran = True
            logging_utils.logpr("Lost connection screen actions.")

            logging_utils.logpr("Pressing " + INPUT_KEY_LIGHT_ATTACK + " key.    -- Menu selection")
            pyautogui.press(INPUT_KEY_LIGHT_ATTACK)  # Return from lost connection screen to main menu.
            # Checks that the "offline" text is still present.
            while pyautogui.pixelMatchesColor(466, 51, (34, 62, 86)) and pyautogui.pixelMatchesColor(497, 45, (14, 19, 50)):
                logging_utils.logpr("Pressing " + INPUT_KEY_LIGHT_ATTACK + " key.  -- Menu selection")
                pyautogui.press(INPUT_KEY_LIGHT_ATTACK)
                logging_utils.logpr("Sleeping inputs for 2 seconds.")
                time.sleep(2)            

def position_testing():
    while True:
        pos = pyautogui.position()
        pix = pyautogui.pixel(pos[0], pos[1])
        logging_utils.logpr("POS: (" + str(pos[0]) + ", " + str(pos[1]) + "), RGB: (" + str(pix[0]) + ", " + str(pix[1]) + ", " + str(pix[2]) + ")")
        time.sleep(1)
