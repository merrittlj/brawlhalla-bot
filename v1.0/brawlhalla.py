#!/usr/bin/env python3.11

from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller
import time, threading, random, pyautogui, sys

toggle_key_combination = '<ctrl>+q'
running = False

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

logging_header = '[brawlhalla.py]: '
input_dictionary = {  # Input choices/Brawlhalla controls.
    'a': "Move left",
    'd': "Move right",
    'w': "Aim up",
    's': "Down",

    'r': "Jump",

    'h': "Light attack",
    'j': "Heavy attack",
    'k': "Throw/pickup",
    'l': "Dodge/dash",
}

selection_key = None
up_key = None
back_key = None
for input_key, description in input_dictionary.items():
    if description == "Light attack":  # Light attack is used as the selection key.
        selection_key = input_key
    if description == "Aim up":  # Aim up used to go up in menus.
        up_key = input_key
    if description == "Dodge/dash":  # Dodge/dash used to go back in menus.
        back_key = input_key

running_event = threading.Event()
listener = keyboard.Listener()
keyboard_input = Controller()

thread_one = None 
thread_two = None


def for_canonical(func):  # Returns a lambda function that "translates" the argument(key) cannonically, and passes it into the original passed function.
    return lambda key: func(listener.canonical(key))

def toggle_hotkey_activated():
    print("\n" + logging_header + "Toggle hotkey " + toggle_key_combination + " activated.")
    
    global running
    running = not running
    if running:            
        running_event.set()

        print(logging_header + "Starting bot.\n")
    else:
        running_event.clear()

        print(logging_header + "Stopping bot.\n")

def main():
    global thread_one
    global thread_two
    
    thread_one = threading.Thread(target = auto_ffa_scout)
    thread_two = threading.Thread(target = auto_ffa_inputs)
    # thread_three = threading.Thread(target = position_testing)
    
    toggle_hotkey = keyboard.HotKey(keyboard.HotKey.parse(toggle_key_combination), toggle_hotkey_activated)
    with keyboard.Listener(
            on_press = for_canonical(toggle_hotkey.press),  # In this scenario, keys are translated cannonically before being passed into "hotkey.press".
            on_release = for_canonical(toggle_hotkey.release)
    ) as listener:
        listener.wait()
        print(logging_header + "Ready to run.")
        thread_one.start()
        # thread_three.start()
        listener.join()

def run_random_inputs():
    while True:
        if running_event.is_set():
            rand_input, input_description = random.choice(list(input_dictionary.items()))
            rand_time = random.randint(5, 25) / 100  # Generate times 0.05 .. 0.25 seconds.

            print(logging_header
                  + "Inputting key: \'" + rand_input
                  + "\' for " + str(rand_time) + " shheconds. "
                  + (" " * (4 - len(str(rand_time)))) + "-- "
                  + input_description)
                
            pyautogui.keyDown(rand_input)
            time.sleep(rand_time)
            pyautogui.keyUp(rand_input)

def auto_ffa_scout():
    global location_states
    global state_index
    global state_action_ran
    global thread_two

    while True:
        if running_event.is_set():
            for i in range(0, 5):
                print(logging_header + "Running auto-FFA in " + str(5 - i) + " seconds.")
                time.sleep(1)

            break
        
    print("\n")            
    thread_two.start()

    while True:
        # Matching pixels on a 600x450 window(X nested server).
        if pyautogui.pixelMatchesColor(135, 38, (168, 127, 105)) and pyautogui.pixelMatchesColor(128, 40, (166, 124, 102)):  # We are in the legend selection. Checks two brown pixels on the far left of the top game-UI.
            print(logging_header + "Pixels matched for legend selection.")
            if state_index == GAME_OVER_SCREEN:
                state_index = LEGEND_SELECTION
                state_action_ran = False
            elif state_index != LEGEND_SELECTION and state_index != LOST_CONNECTION_SCREEN:  # Legend selection may appear when attempting to restore connection.
                print(logging_header + "Incorrect state " + location_states[state_index] + " when state should be legend selection or game over screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(407, 48, (252, 252, 252)) and pyautogui.pixelMatchesColor(410, 44, (235, 235, 235)):  # We are in an active match. Checks two white pixels in the game timer.
            print(logging_header + "Pixels matched for an active match.")
            if state_index == LEGEND_SELECTION:
                state_index = FIRST_ACTIVE_MATCH
                state_action_ran = False
            elif state_index == REJOIN_SCREEN:
                state_index = SECOND_ACTIVE_MATCH
                state_action_ran = False
            elif state_index != FIRST_ACTIVE_MATCH and state_index != SECOND_ACTIVE_MATCH and state_index != PAUSE_SCREEN:  # Pause screen can match active match pixels.
                print(logging_header + "Incorrect state " + location_states[state_index] + " when state should be legend selection, rejoin screen, first active match, pause screen, or second active match. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(403, 387, (0, 0, 51)) and pyautogui.pixelMatchesColor(345, 63, (96, 152, 171)):  # We are in the pause screen. Checks dark blue pause screen background pixel and options text cyan color.
            print(logging_header + "Pixels matched for the pause screen.")
            if state_index == FIRST_ACTIVE_MATCH:
                state_index = PAUSE_SCREEN
                state_action_ran = False
            elif state_index != PAUSE_SCREEN:
                print(logging_header + "Incorrect state " + location_states[state_index] + " when state should be first active match or pause screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(418, 219, (56, 55, 62)) and pyautogui.pixelMatchesColor(450, 209, (0, 0, 51)):  # We are in the rejoin screen. Checks rejoin UI background dark blue pixel and rejoin UI button grey pixel.
            print(logging_header + "Pixels matched for the rejoin screen.")
            if state_index == PAUSE_SCREEN:
                state_index = REJOIN_SCREEN
                state_action_ran = False
            elif state_index == LOST_CONNECTION_SCREEN:
                print(logging_header + "Pressing " + back_key + " key.  -- Menu back")
                pyautogui.press(back_key)
            elif state_index != REJOIN_SCREEN:
                print(logging_header + "Incorrect state " + location_states[state_index] + " when state should be pause screen or rejoin screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(574, 49, (219, 207, 82)) and pyautogui.pixelMatchesColor(462, 44, (52, 42, 128)):  # We are in the game over screen. Checks yellow pixel on coin symbol and background pixel on default avatar.
            print(logging_header + "Pixels matched for the game over screen.")
            if state_index == SECOND_ACTIVE_MATCH:  # Was in an active match, now in the game over screen.
                state_index = GAME_OVER_SCREEN
                state_action_ran = False
            elif state_index != GAME_OVER_SCREEN and state_index != REJOIN_SCREEN and state_index != LOST_CONNECTION_SCREEN:  # Game over pixels can sometimes appear after the rejoin screen, which we want to ignore.
                print(logging_header + "Incorrect state " + location_states[state_index] + " when state should be second active match or game over screen. Exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(310, 187, (241, 210, 1)) and pyautogui.pixelMatchesColor(377, 262, (0, 0, 51)):  # We are in the lost connection screen. Checks yellow pixel on warning symbol and dark blue background pixel on warning UI.
            print(logging_header + "Pixels matched for the lost connection screen.")
            state_index = LOST_CONNECTION_SCREEN
            state_action_ran = False

        print (logging_header + "Current FFA state: " + location_states[state_index] + ", internal number: " + str(state_index) + ".")
        if state_index == LOST_CONNECTION_SCREEN:
            pix1 = pyautogui.pixel(466, 51)
            pix2 = pyautogui.pixel(497, 45)
            print(logging_header + "POS1(466, 51): (" + pix1[0] + ", " + pix1[1] + ", " + pix1[2] + ") POS2(497, 45): (" + pix2[0] + ", " + pix2[1] + ", " + pix2[2] + ")")
                
        time.sleep(1)

def auto_ffa_inputs():
    global location_states
    global state_index
    global state_action_ran
    
    print(logging_header + "Running auto-FFA inputs.")
    
    while True:
        if state_action_ran:
            continue
        
        elif state_index == LEGEND_SELECTION:
            state_action_ran = True
            print(logging_header + "Legend selection actions.")

            print(logging_header + "Pressing " + selection_key + " key every 0.5 seconds 3 times.  -- Menu selection")
            pyautogui.press(selection_key, presses = 3, interval = 0.5)
        
        elif state_index == FIRST_ACTIVE_MATCH:
            state_action_ran = True
            print(logging_header + "Initial active game actions.")

            print(logging_header + "Sleeping inputs for 5 seconds.")
            time.sleep(5)

            while state_index != PAUSE_SCREEN:
                print(logging_header + "Pressing ESC key.  -- Pause menu")
                pyautogui.press('esc')
                print(logging_header + "Sleeping inputs for 1 second.")
                time.sleep(1)

        elif state_index == PAUSE_SCREEN:  # Variable amount of ESC key presses.
            state_action_ran = True
            print(logging_header + "Pause screen actions.")

            print(logging_header + "Pressing " + up_key + " key.    -- Menu up")
            pyautogui.press(up_key)

            print(logging_header + "Sleeping inputs for 0.5 seconds.")
            time.sleep(0.5)

            print(logging_header + "Pressing " + selection_key + " key.    -- Menu selection")
            pyautogui.press(selection_key)

        elif state_index == REJOIN_SCREEN:
            state_action_ran = True
            print(logging_header + "Rejoin screen actions.")

            print(logging_header + "Sleeping inputs for 6 seconds.")
            time.sleep(6)

            print(logging_header + "Pressing " + selection_key + " key every 0.1 seconds 2 times.  -- Menu selection")
            pyautogui.press(selection_key, presses = 2, interval = 0.05)

        elif state_index == GAME_OVER_SCREEN:  # Variable amount of menus to go through.
            state_action_ran = True
            print(logging_header + "Game over actions.")

            while state_index == GAME_OVER_SCREEN:
                print(logging_header + "Pressing " + selection_key + " key.  -- Menu selection")
                pyautogui.press(selection_key)
                
                print(logging_header + "Sleeping inputs for 1 second.")
                time.sleep(1)

        elif state_index == LOST_CONNECTION_SCREEN:  # Attempts to restore connection periodically.
            state_action_ran = True
            print(logging_header + "Lost connection screen actions.")

            print(logging_header + "Pressing " + selection_key + " key.    -- Menu selection")
            pyautogui.press(selection_key)  # Return from lost connection screen to main menu.
            # Checks that the "offline" text is still present.
            while pyautogui.pixelMatchesColor(466, 51, (34, 62, 86)) and pyautogui.pixelMatchesColor(497, 45, (14, 19, 50)):
                print(logging_header + "Pressing " + selection_key + " key.  -- Menu selection")
                pyautogui.press(selection_key)
                print(logging_header + "Sleeping inputs for 2 seconds.")
                time.sleep(2)

            

def position_testing():
    while True:
        pos = pyautogui.position()
        pix = pyautogui.pixel(pos[0], pos[1])
        print("POS: (" + str(pos[0]) + ", " + str(pos[1]) + "), RGB: (" + str(pix[0]) + ", " + str(pix[1]) + ", " + str(pix[2]) + ")")
        time.sleep(1)

if __name__ != "__main__":
    sys.exit(logging_header + "Only use \"brawlhalla.py\" as a script!")
else:
    main()
