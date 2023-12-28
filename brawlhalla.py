#!/usr/bin/env python3.11

from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller
import time, threading, random, pyautogui, sys

toggle_key_combination = '<ctrl>+q'
running = False

location_states = ["Legend selection", "Active match", "Rejoin screen", "Active match", "Game Over"]
state_index = 0
state_action_ran = False

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
for input_key, description in input_dictionary.items():
    if description == "Light attack":  # Light attack is used as the selection key.
        selection_key = input_key
    if description == "Aim up":  # Aim up used to go up in menus.
        up_key = input_key

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
        for i in range(0, 5):
            print(logging_header + "Starting inputs in " + str(5 - i) + " seconds.")
            time.sleep(1)
        print("\n")
            
        running_event.set()
    else:
        running_event.clear()

        print(logging_header + "Stopping inputs.\n")

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
                  + "\' for " + str(rand_time) + " seconds. "
                  + (" " * (4 - len(str(rand_time)))) + "-- "
                  + input_description)
                
            keyboard_input.press(rand_input)
            time.sleep(rand_time)
            keyboard_input.release(rand_input)

def auto_ffa_scout():
    global location_states
    global state_index
    global state_action_ran
    global thread_two
    
    for i in range(0, 5):
            print(logging_header + "Running auto-FFA in " + str(5 - i) + " seconds.")
            time.sleep(1)
    print("\n")
    
    thread_two.start()

    while True:
        if pyautogui.pixelMatchesColor(2375, 922, (167, 141, 122)) and pyautogui.pixelMatchesColor(2372, 924, (169, 151, 137)):  # We are in the legend selection. Checks two brown pixels on the far left of the top game-UI.
            print(logging_header + "Pixels matched for legend selection.")
            if state_index == 4:  # Was in game over state, now in legend selection.
                state_index = 0
                state_action_ran = False
            elif state_index != 0:
                print(logging_header + "Incorrect state " + str(state_index) + " when state should be 0 or 4, exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(2669, 941, (218, 218, 218)) and pyautogui.pixelMatchesColor(2668, 944, (244, 244, 244)):  # We are in an active match. Checks two white pixels in the game timer.
            print(logging_header + "Pixels matched for an active match.")
            if state_index == 0:  # Was in legend selection, now in an active match.
                state_index = 1
                state_action_ran = False
            elif state_index == 2:  # Was in the rejoin screen, now in an active match.
                state_index = 3
                state_action_ran = False
            elif state_index != 1 and state_index != 3:
                print(logging_header + "Incorrect state " + str(state_index) + " when state should be 0 or 1 or 2 or 3, exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(2683, 1111, (56, 55, 62)) and pyautogui.pixelMatchesColor(2725, 1110, (0, 0, 51)):  # We are in the rejoin screen. Checks rejoin UI background dark blue pixel and rejoin UI button pixel.
            print(logging_header + "Pixels matched for the rejoin screen.")
            if state_index == 1:  # Was in an active match, now in the rejoin screen.
                state_index = 2
                state_action_ran = False
            elif state_index != 2:
                print(logging_header + "Incorrect state " + str(state_index) + " when state should be 1 or 2, exitting.")
                sys.exit()

        elif pyautogui.pixelMatchesColor(2848, 933, (199, 171, 78)) and pyautogui.pixelMatchesColor(2729, 930, (52, 42, 128)):  # We are in the game over screen. Checks yellow pixel on coin symbol and background pixel on default avatar.
            print(logging_header + "Pixels matched for the game over screen.")
            if state_index == 3:  # Was in an active match, now in the game over screen.
                state_index = 4
                state_action_ran = False
            elif state_index != 4:
                print(logging_header + "Incorrect state " + str(state_index) + " when state should be 3 or 4, exitting.")
                sys.exit()

        print (logging_header + "Current FFA state: " + str(state_index) + " " + location_states[state_index] + ".")
                
        time.sleep(1)

def auto_ffa_inputs():
    global location_states
    global state_index
    global state_action_ran
    
    print(logging_header + "Running auto-FFA inputs.")
    
    while True:
        if state_action_ran:
            continue
        
        elif state_index == 0:  # Legend selection
            state_action_ran = True
            print(logging_header + "Legend selection actions.")

            for i in range(0, 3):
                print(logging_header + "Inputting " + selection_key + " key.  -- Menu selection")
                keyboard_input.press(selection_key)
                time.sleep(0.1)
                keyboard_input.release(selection_key)
                print(logging_header + "Sleeping inputs for 0.5 seconds.")
                time.sleep(0.5)
        
        elif state_index == 1:  # Active game.
            state_action_ran = True
            print(logging_header + "Initial active game actions.")

            print(logging_header + "Sleeping inputs for 5 seconds.")
            time.sleep(5)

            for i in range(0, 2):
                print(logging_header + "Inputting ESC key.  -- Pause menu")
                keyboard_input.press(Key.esc)  # Go to the menu.
                time.sleep(0.5)
                keyboard_input.release(Key.esc)

            print(logging_header + "Sleeping inputs for 0.5 seconds.")
            time.sleep(0.5)

            print(logging_header + "Inputting " + up_key + " key.    -- Menu up")
            keyboard_input.press(up_key)  # Hover over the exit button.
            time.sleep(0.1)
            keyboard_input.release(up_key)

            print(logging_header + "Inputting " + selection_key + " key.    -- Menu selection")
            keyboard_input.press(selection_key)  # Exit to the main menu/rejoin screen.
            time.sleep(0.1)
            keyboard_input.release(selection_key)

        elif state_index == 2:  # Rejoin screen.
            state_action_ran = True
            print(logging_header + "Rejoin screen actions.")

            print(logging_header + "Sleeping inputs for 6 seconds.")
            time.sleep(6)

            for i in range(0, 2):
                print(logging_header + "Inputting " + selection_key + " key.  -- Menu selection")
                keyboard_input.press(selection_key)  # Go back into the active game.
                time.sleep(0.05)
                keyboard_input.release(selection_key)
                time.sleep(0.1)

        elif state_index == 4:  # Game over. Variable amount of menus to go through.
            state_ran_action = True
            print(logging_header + "Game over actions.")

            while (state_index == 4):
                print(logging_header + "Inputting " + selection_key + " key.  -- Menu selection")
                keyboard_input.press(selection_key)  # Go through the variable amount of menus after the game.
                time.sleep(0.1)
                keyboard_input.release(selection_key)
                print(logging_header + "Sleeping inputs for 1 second.")
                time.sleep(1)

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
