#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using webbrowser library (Interfaces for launching and remotely 
controlling Web browsers - comes with python)
"""

import sys
import argparse
import webbrowser
from validators import url
from time import sleep

__email__ = "knifef@protonmail.com"

BASE_URL = "https://docs.python.org/3.1/library/webbrowser.html"

if len(sys.argv) > 1:
    # Object for parsing command line strings into Python objects.
    parser = argparse.ArgumentParser()
    # Adding argument actions
    parser.add_argument("-u", "--URL", dest="given_urls", type=str, nargs='*',
                        help="Enter URLs to open them in new tabs of your browser")
    args = parser.parse_args()  # Command line argument parsing methods
    given_urls = args.given_urls

    for current_url in given_urls:
        if url(current_url):  # Return whether or not given value is a valid URL.
            # Open current url in a new “tab” of the browser, if possible, otherwise - in a new window of the browser.
            webbrowser.open_new_tab(current_url)
            sleep(2)  # delay in seconds
else:
    # Open url in a new “tab” of the browser, if possible, otherwise - in a new window of the browser.
    webbrowser.open_new_tab(BASE_URL)
