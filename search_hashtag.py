#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This simple script searches hashtag on twitter (linux and Windows only), using pyautogui,
and saves text from search results to a text file (.txt)
"""

import os
import sys
import codecs
import platform
import pyautogui
import pyperclip
from pathlib import Path
from time import sleep
from validators import url


__author__ = "KnifeF"
__license__ = "MIT"
__email__ = "knifef@protonmail.com"

RESULTS_PATH = os.path.join(str(Path.home()), "DESKTOP", "hashtag_results")  # path to save text file
IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')  # path to imgs folder
TWITTER_SEARCH_URL = "https://twitter.com/search-home?lang=en"  # twitter search URL
HASHTAG = "#java"  # hashtag to search on twitter


def find_platform():
    """
    tries to check if the os platform is linux or windows
    :return: windows, or linux, or platform's info (str)
    """
    # Returns a single string identifying the underlying platform
    # with as much useful information as possible
    platform_info = platform.platform()

    if platform_info.lower().startswith("win"):
        return "windows"
    elif platform_info.lower().startswith("linux"):
        return "linux"
    return platform_info


def open_url_from_cmd(given_url):
    """
    hit Win+R shortcut, run 'Command Prompt' (CLI), and open given url on default browser.
    :param given_url: url to type & open with cmd
    :return:
    """
    if url(given_url):
        pyautogui.hotkey('winleft', 'r')  # shortcut to open 'Run'
        sleep(1)
        pyautogui.typewrite('cmd', interval=0.1)  # type 'cmd'
        pyautogui.press('enter')  # hit 'Enter' (to open cmd)
        sleep(2)
        pyautogui.typewrite('start %s && exit' % given_url, interval=0.1)  # type command to open url & exit cmd
        pyautogui.press('enter')  # execute command
        sleep(5)


def open_url_from_terminal(given_url):
    """
    hit Ctrl+Alt+T shortcut to run 'Terminal' (CLI), and open given url on default browser.
    :param given_url: url to type & open with terminal
    :return:
    """
    if url(given_url):
        pyautogui.hotkey('ctrlleft', 'altleft', 't')  # shortcut to open terminal
        sleep(2)
        pyautogui.typewrite('xdg-open %s && exit' % given_url, interval=0.1)  # type command to open url & exit cmd
        pyautogui.press('enter')  # execute command
        sleep(5)


def get_current_url(platform_name):
    """
    tries to get current URL of default opened browser (using pyautogui and pyperclip)
    :param platform_name: should contain the name of the OS platform - win/linux (str)
    :return: (str) current url in browser, or None
    """
    if "linux" in platform_name:
        pyautogui.hotkey("ctrlleft", "l")
    elif "win" in platform_name:
        pyautogui.hotkey("altleft", "d")  # Go to Address Bar shortcut
    else:
        return None

    sleep(1)
    pyautogui.hotkey("ctrlleft", "c")  # copy shortcut
    current_url = pyperclip.paste()  # using pyperclip to paste text from clipboard to a variable
    pyautogui.press('tab')  # hit tab to return from Address Bar
    if url(current_url):
        return current_url
    else:
        return None


def locate_and_click(path):
    """
    tries to locate image/pattern on screen, move the cursor, and click on the center of it.
    :param path:
    :return:
    """
    # path exists, is file, and ends with 'png' extension
    if path and path.endswith('.png') and os.path.exists(path) and os.path.isfile(path):
        # locate image/pattern on screen
        search_box = pyautogui.locateOnScreen(path, minSearchTime=5)
        if search_box:
            loc_x, loc_y = pyautogui.center(search_box)  # center of found image loc
            # Moves the mouse cursor to a point on the screen
            pyautogui.moveTo(x=loc_x, y=loc_y, duration=4.0)
            # performs pressing a mouse button down and then immediately releasing it
            pyautogui.click(x=loc_x, y=loc_y)
            return True
    return False


def search_hashtag(hashtag):
    """
    searches an hashtag - should be used when search box element is focused (in twitter search)
    :param hashtag: (str) hashtag to search, for example: #python or #helloworld
    :return: (boolean) True - if found search box and searched hashtag, or False
    """
    if locate_and_click(os.path.join(IMG_PATH, 'search_q.png')):  # click on search box element if visually found
        pyautogui.typewrite('%s' % hashtag, interval=0.4)  # should type the hashtag inside search box
        pyautogui.press('enter')  # hit enter to search the hashtag
        return True
    return False


def save_visible_text_area(file_name):
    """
    copy all visible text area to a variable, and save text to a file
    :param file_name: file name to save text file
    :return:
    """
    pyautogui.hotkey("ctrlleft", "a")  # mark area shortcut
    sleep(1)
    pyautogui.hotkey("ctrlleft", "c")  # copy shortcut
    sleep(2)
    text_from_page = pyperclip.paste()  # using pyperclip to paste text from clipboard to a variable

    if text_from_page and file_name.endswith(".txt"):  # filename not None, and ends with '.txt' extension
        create_dir(RESULTS_PATH)  # create dirs in path
        sleep(1)
        if os.path.exists(RESULTS_PATH) and os.path.isdir(RESULTS_PATH):  # dir exists
            # save data from variable to a text file
            with codecs.open(os.path.join(RESULTS_PATH, file_name), "w", encoding='utf-8') as f:
                f.write(text_from_page)  # write string to stream
            f.close()


def create_dir(path):
    """
    Test whether a path exists, and create dirs in path (if not exist).
    :param path: path to check whether it exists or not.
    :return:
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("OS Error")
        # Exit the interpreter by raising SystemExit(status).
        sys.exit("Error: failed to create a directory on desktop.")
        pass


def main():
    """
    The main function
    :return:
    """
    platform_name = find_platform()
    if platform_name:
        if platform_name == "windows":
            open_url_from_cmd(TWITTER_SEARCH_URL)
        elif platform_name == "linux":
            open_url_from_terminal(TWITTER_SEARCH_URL)
        else:
            sys.exit("this script is probably not compatible with your OS platform")

        current_url = get_current_url(platform_name)
        if current_url and "https://twitter.com/search" in current_url:
            if search_hashtag(HASHTAG):
                sleep(5)
                results_url = get_current_url(platform_name)
                if results_url and ("https://twitter.com/search?q=" in results_url):
                    save_visible_text_area(HASHTAG.replace("#", "")+".txt")
                    pyautogui.hotkey("ctrlleft", "w")  # to close browser's window

if __name__ == '__main__':
    main()
