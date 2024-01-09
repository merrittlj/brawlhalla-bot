#!/usr/bin/env python3

import os, sys

# Local imports
# From game/
# from brawlhalla_bot_merrittlj.game import brawlhalla_bot

# From util/
from brawlhalla_bot_merrittlj.util import logging_utils
from brawlhalla_bot_merrittlj.util import hotkey_utils

# From config/
from brawlhalla_bot_merrittlj.config import brawlhalla_config 


def main():
    bot_inputs = [brawlhalla_config.INPUT_KEY_LEFT, brawlhalla_config.INPUT_KEY_RIGHT, brawlhalla_config.INPUT_KEY_AIM_UP, brawlhalla_config.INPUT_KEY_DOWN, brawlhalla_config.INPUT_KEY_JUMP, brawlhalla_config.INPUT_KEY_LIGHT_ATTACK, brawlhalla_config.INPUT_KEY_HEAVY_ATTACK, brawlhalla_config.INPUT_KEY_THROW, brawlhalla_config.INPUT_KEY_DODGE]
    # bot = brawlhalla_bot.FFA_Bot(bot_inputs)

    bot_hotkey = hotkey_utils.Hotkey(brawlhalla_config.TOGGLE_KEY_COMBINATION, lambda : logging_utils.logpr("ONESHOT hotkey is activated."), hotkey_utils.Hotkey_Modes.ONESHOT)
    bot_hotkey.run()

    
if __name__ == "__main__":
    print("\n")
    main()
    print("\n")
else:
    logging_utils.logpr(f"Only use \"{os.path.basename(__file__)}\" as a script!")
    sys.exit()
