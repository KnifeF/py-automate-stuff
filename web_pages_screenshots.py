#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This simple script navigates to URL addresses by a given input (using Selenium WebDriver with Firefox),
and takes several screenshots from the web pages (scrolls down each page to get more data on screen).

The script might be useful for documentation of screenshots from required web pages.

An input from command prompt/terminal should look like:
python your\path\to\web_pages_screenshots.py -u "https://selenium-python.readthedocs.io"
"https://www.seleniumhq.org/docs/"

-OR-

python your\path\to\web_pages_screenshots.py --URL
"https://selenium-python.readthedocs.io" "https://www.seleniumhq.org/docs/"
"""

import os
import sys
import argparse
import pyscreenshot as img_grab
from selenium import webdriver
from validators import url
from slugify import slugify
from time import sleep
from random import randint

__author__ = "KnifeF"
__license__ = "MIT"
__email__ = "knifef@protonmail.com"

# path to WebDriver for Firefox ('geckodriver.exe')
GECKO_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geckodriver')
SCREENSHOTS_PATH = os.path.join(os.environ["HOMEPATH"], "DESKTOP", "all_screenshots")
TEST_URLS = ['https://selenium-python.readthedocs.io',
             'https://selenium-python.readthedocs.io/installation.html']


class WebPagesScreenshots:

    def __init__(self, url_addresses=None):
        """
        creates new instance of WebPagesScreenshots Object
        :param url_addresses: URL addresses to take screenshots from (list)
        """
        self.url_addresses = []
        if url_addresses and isinstance(url_addresses, list):  # param is a list (not None)
            # trying to initialize list from given param (if the list includes URLs)
            for given_url in url_addresses:
                # val is a string (not None), and is a valid URL
                if given_url and isinstance(given_url, str) and url(given_url):
                    self.url_addresses.append(given_url)  # append object to end of list

        if not self.url_addresses:
            self.url_addresses = TEST_URLS  # initialize list of URLs from a default list

        # Creates a new instance of the firefox driver.
        self.driver = webdriver.Firefox(executable_path=GECKO_DRIVER_PATH)
        self.driver.maximize_window()  # Maximizes the current window that webdriver is using

        if not create_dir(SCREENSHOTS_PATH):  # create dir/dirs if not exist
            # Exit the interpreter by raising SystemExit(status).
            sys.exit("Error: failed to create a directory on desktop.")

    def scroll_down_and_grab_screen(self):
        """
        scrolling page down with selenium WebDriver to get more data from target url,
        and taking screenshots from page.
        :return:
        """
        if self.driver:
            page_title = self.driver.title  # Returns the title of the current page
            page_title = slugify(page_title, lowercase=False)  # Make a slug from the given text

            # creates dir path to save web page screenshots
            current_dir_path = os.path.join(SCREENSHOTS_PATH, page_title)
            if not create_dir(current_dir_path):
                return

            # get height of the current window and divide by 2
            half_window_height = str(self.driver.get_window_size()['height']/2)

            # window.pageYOffset - the number of pixels that the document has already been scrolled from the
            # upper left corner of the window, vertically (scrolled height)
            last_scrolling_height = self.driver.execute_script("return window.pageYOffset;")

            count = 0
            scr = 0
            while scr < 100:  # 100 screenshots limit for loop

                # count should stay zero while scrolled height is changing (after scrolling)
                if count == 0:
                    # takes a screenshot and saves image to file
                    take_a_screenshot(os.path.join(current_dir_path,
                                                   "%s - %s.png" % (page_title, "scr"+str(scr))))
                    scr += 1

                sleep(1)  # delay in seconds

                # Scroll down to bottom
                self.driver.execute_script("window.scrollBy(0,"+half_window_height+");")

                # Wait to load page
                sleep(randint(1, 2))  # delay in seconds

                # get height of 'window.pageYOffset' after scrolling, and compare with last page's scroll height
                new_scrolling_height = self.driver.execute_script("return window.pageYOffset;")

                # same height after scrolling page down
                if new_scrolling_height == last_scrolling_height:
                    count += 1
                    if count >= 3:
                        sleep(randint(1, 2))
                        break  # exit while-loop
                else:
                    count = 0
                # updating the last scrolled height, before another scrolling
                last_scrolling_height = new_scrolling_height
            print("<-- finished scrolling page --> ", self.driver.current_url)


def take_a_screenshot(file_path):
    """
    takes a screenshot and saves image to file
    :param file_path: the path of the output file (string)
    :return:
    """
    try:
        # Copy the contents of the screen to PIL image memory (grab full screen)
        im = img_grab.grab()
        # Saves this image under the given filename.
        im.save(file_path)
    except (KeyError, IOError, Exception):
        print("An error occurred while trying to take a screenshot")
        pass


def create_dir(path):
    """
    Test whether a path exists, and create dirs in path (if not exist).
    :param path: path to check whether it exists or not.
    :return: boolean - True if path exists, or False
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except OSError:
        print("OS Error")
        return False


def get_user_inputs():
    """
    tries to get user's inputs
    :return: list of inputs from the user (list of strings)
    """
    input_lst = []
    attempts = 0
    while attempts <= 5:
        attempts += 1
        try:
            value = input("enter a url or 'quit': ")
        except ValueError:
            print("You entered an invalid input.")
            continue

        if (value.lower() == 'quit') or (value.lower() == 'q'):
            sys.exit(0)  # Exit the interpreter by raising SystemExit(status).
        else:
            input_lst.append(value)

    return input_lst


def main():
    """
    The main function:
    Scroll down web pages (from given URL) and take some screenshots from different parts on each page.
    :return:
    """
    if len(sys.argv) > 1:
        # Object for parsing command line strings into Python objects.
        parser = argparse.ArgumentParser()
        # Adding argument actions
        parser.add_argument("-u", "--URL", dest="given_urls", type=str, nargs='*',
                            help="Enter URLs to take screenshots from the required web pages")
        args = parser.parse_args()  # Command line argument parsing methods
        given_urls = args.given_urls
    else:
        given_urls = get_user_inputs()  # tries to get a URL address as input from the user

    if given_urls:
        wp_scrs = WebPagesScreenshots(given_urls)  # creates new instance of WebPagesScreenshots Object
        if wp_scrs and wp_scrs.url_addresses:
            for current_url in wp_scrs.url_addresses:
                wp_scrs.driver.get(current_url)  # Loads a web page in the current browser session
                wp_scrs.scroll_down_and_grab_screen()  # scroll down page & take screenshots
                sleep(2)
        wp_scrs.driver.quit()  # Quits the driver and close every associated window

if __name__ == '__main__':
    main()
