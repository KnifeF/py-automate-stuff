#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Attempt to make a reverse image search with google, using PyAutoGUI (Cross-platform GUI automation for human 
beings), webbrowser (Interfaces for launching and remotely controlling Web browsers), and unittest (Python unit 
testing framework) libraries.

The script tries to upload a photo to google image search (drag&drop), and to check if the photo is found on web,
using PyAutoGUI's GUI automation&image recognition abilities.
"""

import os
import sys
import subprocess
import unittest
import webbrowser
import pyautogui
import pyperclip
from time import sleep
from random import randint

__author__ = "KnifeF"
__email__ = "knifef@protonmail.com"

BASE_URL = "https://www.google.co.il/imghp?hl=en&tab=wi"  # base url to get  (Google image search URL)
IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')  # path to imgs folder
IMG_NAME = "actor"  # image filename to search with google


class TestGoogleImageSearch(unittest.TestCase):  # A class whose instances are single test cases.

    @unittest.skipUnless(sys.platform.lower().startswith("win"), "requires Windows")
    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        :return:
        """
        try:
            self.upload_img_path = os.path.join(IMG_PATH, 'google_upload_img.png')  # path to upload img path
            self.required_photo_path = os.path.join(IMG_PATH, '%s.jpg' % IMG_NAME)  # path to required image
            # path to image (the check mark should be seen when a file is selected)
            self.selected_photo_path = os.path.join(IMG_PATH, 'selected_file.png')
            # path to image (search by image pattern - in google image search)
            self.search_by_img_path = os.path.join(IMG_PATH, 'search_by_img.png')

            # Check the expressions are true.
            self.assertTrue(self.upload_img_path.endswith('.png') and self.required_photo_path.endswith('.jpg')
                            and self.selected_photo_path.endswith('.png') and self.search_by_img_path.endswith('.png'))
            self.assertTrue(os.path.isfile(self.upload_img_path) and os.path.isfile(self.required_photo_path)
                            and os.path.isfile(self.selected_photo_path) and os.path.isfile(self.search_by_img_path))

        except AssertionError or Exception as e:
            sys.exit("setUp failed! --> %s" % e)

    @unittest.skipUnless(sys.platform.lower().startswith("win"), "requires Windows")
    def tearDown(self):
        pyautogui.hotkey('ctrl', 'w')

    @unittest.skipUnless(sys.platform.lower().startswith("win"), "requires Windows")
    def test_google_image_search(self):
        """
        tries to upload a photo to google image search (drag&drop),
        and to check if the photo is found on web.
        :return:
        """
        try:
            # --------------open browser with given url - google's reverse image search--------
            pyautogui.hotkey('win', 'm')  # shortcut to minimize all windows
            # Open current url in a new “tab” of the browser (also checks that the expression is true)
            self.assertTrue(webbrowser.open_new_tab(BASE_URL))
            sleep(3)  # delay (wait for page to load)
            pyautogui.hotkey('win', 'up')  # shortcut to maximize browser's window
            pyautogui.hotkey('win', 'up')  # shortcut to maximize window
            sleep(3)  # delay
            print("browser is now opened!")

            # --------------locate and click on upload image button (on google's reverse image search)----------
            # locate image/pattern on screen (upload image button)
            img_upload = pyautogui.locateOnScreen(self.upload_img_path, minSearchTime=10)
            self.assertIsNotNone(img_upload)  # Included for symmetry with assertIsNone
            loc_x, loc_y = pyautogui.center(img_upload)  # center of found image/pattern loc
            # Moves the mouse cursor to a given point (x,y) on the screen
            pyautogui.moveTo(x=loc_x, y=loc_y, duration=4.0)
            # performs pressing a mouse button down and then immediately releasing it
            pyautogui.click(x=loc_x, y=loc_y)
            print("clicked on upload image button!")
            sleep(3)  # delay
            pyautogui.hotkey('win', 'right')  # shortcut to move window to left/right/up/down workspace
            sleep(1)  # delay

            # --------------find and show the required image file in folder (in explorer)---------------
            # Run command with arguments (to find photo on explorer)
            subprocess.Popen(r'explorer /select,%s' % self.required_photo_path)
            print("file is showed up and selected!")
            sleep(2)  # delay
            pyautogui.hotkey('win', 'up')  # shortcut to maximize window
            sleep(1)  # delay
            pyautogui.hotkey('win', 'left')  # shortcut to move window to left/right/up/down workspace
            sleep(1)  # delay

            # --------------a drag&drop operation - drag an image file to search on Google---------------
            # Check that the expression is true
            self.assertTrue(locate_and_move_to(self.selected_photo_path, self.search_by_img_path))
            sleep(1)  # delay
            pyautogui.hotkey('win', 'm')  # minimize all windows
            sleep(1)  # delay
            pyautogui.hotkey('alt', 'tab')  # switch window (next/previous)
            sleep(1)  # delay
            pyautogui.hotkey('win', 'left')  # shortcut to move window to left/right/up/down workspace
            pyautogui.hotkey('win', 'up')  # shortcut to maximize window
            # delay (random time to wait for google search results to appear - might take a while)
            sleep(randint(10, 20))

            # ----copy text from search results, and find out if there are matching images---------------
            pyautogui.hotkey('ctrl', 'a')  # shortcut to select all text area
            sleep(1)  # delay
            pyautogui.hotkey('ctrl', 'c')  # shortcut to copy selected text
            sleep(randint(2, 5))  # delay
            copied_text = pyperclip.paste()  # get data from clipboard, to a variable
            # Just like self.assertTrue(a in b), but with a nicer default message.
            # trying to find text in copied text.
            self.assertIn("pages that include matching images", copied_text.lower())
            print("the given image is found on web!")

        except AssertionError or Exception as e:
            sys.exit("test_google_images failed! --> %s" % e)


def locate_and_move_to(from_path, to_path):
    """
    tries to locate image/pattern on screen, and move the cursor to it's location.
    :return:
    """
    # paths exist, are files, and end with a 'png' extension
    if (from_path and to_path) and (from_path.endswith('.png') and to_path.endswith('.png')) \
            and (os.path.exists(from_path) and os.path.exists(to_path)) \
            and (os.path.isfile(from_path) and os.path.isfile(to_path)):

        from_pattern_loc = pyautogui.locateOnScreen(from_path, minSearchTime=10)  # locate image/pattern on screen
        to_pattern_loc = pyautogui.locateOnScreen(to_path, minSearchTime=10)  # locate image/pattern on screen

        if from_pattern_loc and to_pattern_loc:
            from_x, from_y = pyautogui.center(from_pattern_loc)  # center of found image loc
            to_x, to_y = pyautogui.center(to_pattern_loc)  # center of found image loc

            # Moves the mouse cursor to a point on the screen
            pyautogui.moveTo(x=from_x, y=from_y, duration=4.0)
            pyautogui.dragTo(x=to_x+randint(1, 20), y=to_y+randint(1, 20),
                             duration=4.0, button='left')
            return True
    return False


def suite():
    """
    create an instance of TestSuite, then add test case instances.
    :return:  TestSuite obj
    """
    # A test suite is a composite test consisting of a number of TestCases.
    unittest_suite = unittest.TestSuite()
    # add test case to TestSuite
    unittest_suite.addTest(unittest.makeSuite(TestGoogleImageSearch))  # add test
    return suite


if __name__ == '__main__':
    """
    unittest main program
    """
    # A test runner class that displays results in textual form
    runner = unittest.TextTestRunner()
    # create an instance of TestSuite, then add test case instances
    test_suite = suite()
    # Run the given test suite
    result = runner.run(test_suite)
