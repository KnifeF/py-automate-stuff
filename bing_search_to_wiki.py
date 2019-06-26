#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using Selenium WebDriver (FireFox) and unittest library.
The script searches a keyword with 'bing', tries to find a result from 'Wikipedia',
and to save the HTML source of the result from 'Wikipedia'.
"""

import os
import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

__email__ = "knifef@protonmail.com"


FIREFOX_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geckodriver')  # path to webdriver
DESKTOP_PATH = os.path.join(os.environ["HOMEPATH"], "DESKTOP")  # path to desktop
BASE_URL = "https://www.bing.com/"  # base url to get
WIKI_LINK = r"//a[text()[contains(.,'Wikipedia')]]"


class TestSeleniumFireFox(unittest.TestCase):  # A class whose instances are single test cases.

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        :return:
        """
        # Initialises a new instance of a Firefox Profile
        profile = webdriver.FirefoxProfile()
        # sets the preference that we want in the profile (user-agent)
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
        # updates preferences
        profile.update_preferences()

        # Starts a new local session of Firefox.
        self.driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH, firefox_profile=profile)
        self.driver.maximize_window()  # Maximizes the current window that webdriver is using

    def test_bing_search(self):
        """
        tests a keyword search with bing search engine
        :return:
        """
        # Loads a web page in the current browser session.
        self.driver.get(BASE_URL)
        # WebDriver waits up to 10 seconds before throwing a TimeoutException
        # unless it finds the element (search box) to return within 10 seconds.
        search_box = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name('q'))
        sleep(2)  # delay
        # Clears the text if it's a text entry element.
        search_box.clear()
        search_box.send_keys("Unit testing")  # Sends keys to current focused element.
        sleep(1)  # delay
        search_box.send_keys(Keys.ENTER)  # hit Enter to search
        sleep(2)  # delay
        # Just like self.assertTrue(a not in b), but with a nicer default message.
        self.assertNotIn("There are no results for", self.driver.page_source)
        # WebDriver waits up to 10 seconds before throwing a TimeoutException
        # unless it finds the element (search box) to return within 10 seconds.
        link_elem = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_xpath(WIKI_LINK))
        link_elem.click()  # Clicks the element.
        sleep(3)  # delay

        # Just like self.assertTrue(a in b), but with a nicer default message.
        self.assertIn("wikipedia", self.driver.title.lower())
        self.assertIn("assert", self.driver.page_source)

        # Open file and return a stream
        with open(os.path.join(DESKTOP_PATH, "Unit testing - Wikipedia.txt"), "w", encoding='utf-8') as my_file:
            # Gets the source of the current page & writes string to stream.
            my_file.write(self.driver.page_source)
        my_file.close()

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        :return:
        """
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()  # Unittest main program
