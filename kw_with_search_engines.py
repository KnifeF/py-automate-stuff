#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using Selenium WebDriver - and unittest library, 
to search a term with some search engines (yahoo, bing, duckduckgo).
"""

import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

__email__ = "knifef@protonmail.com"

YAHOO_URL = "https://www.yahoo.com/"
BING_URL = "https://www.bing.com/"
DUCKDUCKGO_URL = "https://www.duckduckgo.com/"


class TestSeleniumFireFox(unittest.TestCase):  # A class whose instances are single test cases.

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        :return:
        """
        # Initialises a new instance of MicrosoftWebDriver (Edge browser)
        self.driver = webdriver.Edge()
        self.driver.maximize_window()  # Maximizes the current window that webdriver is using

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        :return:
        """
        # Delete all cookies in the scope of the session.
        self.driver.delete_all_cookies()
        # Quits the driver and closes every associated window.
        self.driver.quit()

    def test_duckduckgo_search(self):
        """
        tests a keyword search with duckduckgo search engine
        :return:
        """
        # Loads a web page in the current browser session.
        self.driver.get(DUCKDUCKGO_URL)
        sleep(3)  # delay
        # Fail if the two objects are unequal as determined by the '==' operator.
        self.assertEqual(self.driver.title, 'DuckDuckGo — Privacy, simplified.')
        # WebDriver waits up to 5 seconds, trying to find an element
        search_box = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_name('q'))
        sleep(2)  # delay
        # Clicks the element.
        search_box.click()
        search_box.send_keys("python")  # Sends keys to current focused element.
        sleep(1)  # delay
        search_box.send_keys(Keys.ENTER)  # hit Enter to search
        sleep(5)  # delay
        # Just like self.assertTrue(a in b), but with a nicer default message.
        self.assertIn("python.org", self.driver.page_source.lower())

    def test_yahoo_search(self):
        """
        tests a keyword search with yahoo search engine
        :return:
        """
        # Loads a web page in the current browser session.
        self.driver.get(YAHOO_URL)
        sleep(3)  # delay
        # Fail if the two objects are unequal as determined by the '==' operator.
        self.assertEqual(self.driver.title, 'Yahoo')
        # WebDriver waits up to 10 seconds before throwing a TimeoutException
        # unless it finds the element (search box) to return within 10 seconds.
        search_box = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_name('p'))
        sleep(2)  # delay
        # Clicks the element.
        search_box.click()
        search_box.send_keys("python")  # Sends keys to current focused element.
        sleep(1)  # delay
        search_box.send_keys(Keys.ENTER)  # hit Enter to search
        sleep(5)  # delay
        # Just like self.assertTrue(a in b), but with a nicer default message.
        self.assertIn("python.org", self.driver.page_source.lower())

    def test_bing_search(self):
        """
        tests a keyword search with bing search engine
        :return:
        """
        # Loads a web page in the current browser session.
        self.driver.get(BING_URL)
        sleep(3)  # delay
        # Fail if the two objects are unequal as determined by the '==' operator.
        self.assertEqual(self.driver.title, 'Bing')
        # WebDriver waits up to 5 seconds, trying to find an element
        search_box = WebDriverWait(self.driver, 5).until(lambda driver: self.driver.find_element_by_name('q'))
        sleep(2)  # delay
        # Clicks the element.
        search_box.click()
        search_box.send_keys("python")  # Sends keys to current focused element.
        sleep(1)  # delay
        search_box.send_keys(Keys.ENTER)  # hit Enter to search
        sleep(5)  # delay
        # Just like self.assertTrue(a in b), but with a nicer default message.
        self.assertIn("python.org", self.driver.page_source.lower())


if __name__ == '__main__':
    unittest.main()  # Unittest main program
