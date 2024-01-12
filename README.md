<h1 align="center">
    <br>
    brawlhalla-bot
    <br>
</h1>
<p align="center">
<p align="center">Smart, stable, efficient Brawlhalla match automation bot.</p>

## Notice
READING ALL OF THE README.MD IS RECOMMENDED TO PROPERLY USE AND UNDERSTAND THIS!

This was originally developed with the intent of personal use and for learning purposes. This is not harmful in any way. No responsibility is taken for any damages that may be caused as a result of this.

## Description/How
This is a automation bot for Brawlhalla free-for-all matches. It works through tracking pixels on the screen and monitoring the game states through this, responding accordingly with the appropriate actions. No memory modification is used here, or anything else cheat-related. This bot simply finds pixels on the screen, and presses keyboard inputs accordingly through pyautogui. If you are paranoid, you can disable EAC within the Steam game launch options by adding `-noeac`.

Technically, this bot is based on a ~~bug~~ feature where leaving a match will replace you with the game's own bot. If you rejoin the match and do not input any buttons, this bot will stay, yet you will be rewarded at the end of the match. While this may sound simple in theory, accounting for stability, varying matchmaking times, lag, and efficiency disallows any approach that may be simpler in code than this.

## Features
* Stable: This bot has multiple features to handle possible UI lag or network disconnections, and automatically deal with these situations accordingly.
* Efficient: This bot runs the required keypresses only when necessary, yet reacts appropriately to special situations.
* Smart: This bot manages and determines in-game state(with no memory-related action) through pixels, and ensures correct functionality for the respective states.
* Large support: Due to the nature of this bot, the same code will work across multiple platforms and resolutions easily, which is a large improvement compared to memory solutions.

## Support
As this uses pyautogui with simple pixel/keyboard actions, this is easilly cross-platform. However, resolution-wise, a list is below. More can be implemented if I desire, but these are the resolutions I use and are supported:
* 1920x1080
* 600x450
To allow the bot to properly match pixels, make sure your game is borderless windowed or fullscreen mode, where the game takes up the entire resolution/screen.

## Problems
Always make sure the bot is correctly working through multiple games before leaving it unattended. The bot is programmed to only use a specific set of inputs and keep to a specific state order, so accidental shop purchases(or similar) are nearly impossible. However, there may be an issue regarding the pixel matching for your screen. If the bot is inactive, observed through no inputs in menu-related states or a lack of console output, please note your system configuration and open an issue in the issues tab with it. I will do my best to help anybody that has problems with the bot.

## Setup
This repository is coded as a python package, due to the nature of how I desired to access and run the bot. Make sure you have Python 3 and git installed before this. Please follow the below instructions:

### Package building
1. To download the project, run:
```
git clone --recurse submodules https://github.com/merrittlj/brawlhalla-bot/ brawlhalla-bot
cd brawlhalla-bot/
```

2. To install this for it's use as a Python package(necessary), make sure the following python modules are installed:
* build
* hatchery
* pynput
* pyautogui

Now run:
```
python3 -m build
pip install --editable .
```

3. As mentioned earlier, this bot runs in the parts of a package and runner. The runner is found(as a submodule) in the `runner` directory of this repository, but it can be installed separately [here](https://github.com/merrittlj/brawlhalla-bot-runner). It requires the `pyyaml` Python module.
```
cd runner/
```

4. If all went well, you should be able to run the bot with the command `python3 runner.py`. But, you most likely desire to configure the bot according to your needs before running:

## Configuration
All configuration for the bot(excluding code modifications) is done through the `runner/config.yaml`(from the base directory of this repository) file. This configuration file is explained below, but comments are included in the configuration file:
* `toggle_key_combination`: The key combination to toggle the bot on and off. The default is "<ctrl>+q".
* `input_key_[xxxx]`: These are your Brawlhalla all-keyboard controls. Please set them accordingly before running the bot.
* `input_keys`: These are the keys that the bot will use(all should be used in the custom-game random input mode, but this is not implemented. See issue #3.). Excluding certain keys here will break the bot in its FFA mode.

## License

Distributed under the Apache License 2.0. See ['LICENSE'](https://github.com/merrittlj/brawlhalla-bot/blob/master/LICENSE) for more info.