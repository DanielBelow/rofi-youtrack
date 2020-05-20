# Rofi youtrack search

## General description

Inspired by [rofi-web-search](https://github.com/pdonadeo/rofi-web-search/). 

Use [Rofi](https://github.com/davatorium/rofi) to search for issues on [YouTrack](https://www.jetbrains.com/youtrack/).

The typed query will be checked for:
- ending with a `!`: shows 10 most recently updated suggestions
- matching a single issue id: directly opens that single issue in the browser
- otherwise: opens the issue tracker with the given search query

## Requirements
- rofi
- python3

## Configuration
Install script dependencies with `pip install -r requirements.txt`.

Add/change your YouTrack token and browser in the script (check [here](https://www.jetbrains.com/help/youtrack/standalone/Manage-Permanent-Token.html#obtain-permanent-token) for help on generating a token).
Using bspwm add the following line to `.config/sxhkd/sxhkdrc`:

    <your_keybind>
        rofi -lines 10 -padding 0 -hide-scrollbar -show search -modi search:/path/to/yt-search.py -i