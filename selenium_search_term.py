#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using Selenium WebDriver (Simulates Microsoft Edge/Mozilla FireFox/Google Chrome browser).
The script searches a given keyword in 'duckduckgo' (search engine), and append links to a text file.
"""

import os
import sys
import argparse
import re
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

__email__ = "knifef@protonmail.com"

# path to locate WebDrivers
EDGE_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MicrosoftWebDriver')
FIREFOX_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geckodriver')
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')

DESKTOP_PATH = os.path.join(os.environ["HOMEPATH"], "DESKTOP")  # path to desktop
DRIVER_TYPES = ['chrome', 'firefox', 'edge']  # list with browsers' names
MORE_RESULTS = r"#rld-1 a"  # css selector to <a> tag
BASE_URL = "https://duckduckgo.com/"  # base url to get


class SearchWithSelenium:
    def __init__(self, kw="selenium", driver_name="chrome"):
        """
        Creates new instance of SearchWithSelenium - simulates chrome/firefox/edge browser,
        using Selenium WebDriver, and tries to search a keyword with 'duckduckgo'
        :param kw: keyword to search (str)
        :param driver_name: given name to choose which WebDriver to simulate (str)
        """
        if not kw:
            kw = "selenium"
        if (not driver_name) or (driver_name not in DRIVER_TYPES):
            driver_name = "chrome"

        self.kw = kw  # keyword to search
        self.driver = None
        self.build_driver(driver_name)

    def build_driver(self, driver_name):
        """
        Creates a new instance of the WebDriver of Chrome/Firefox/Edge
        :param driver_name: given name to choose which WebDriver to simulate (str)
        :return:
        """
        if driver_name == "chrome":
            self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        elif driver_name == "firefox":
            self.driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)
        elif driver_name == "edge":
            self.driver = webdriver.Edge(executable_path=EDGE_DRIVER_PATH)
        else:
            sys.exit("couldn't build WebDriver")

        # Maximizes the current window that webdriver is using
        self.driver.maximize_window()

        # An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying
        # to find any element (or elements) not immediately available.
        self.driver.implicitly_wait(10)

    def search_on_duckduckgo(self):
        """
        search a keyword with duckduckgo and append links from search
        results (HTML from page source) to a text file.
        :return:
        """
        # check whether the WebDriver is Chrome/FireFox/Edge
        if self.driver and (isinstance(self.driver, webdriver.Chrome)
                            or isinstance(self.driver, webdriver.Firefox)
                            or isinstance(self.driver, webdriver.Edge)):

            # Loads a web page in the current browser session.
            self.driver.get(BASE_URL)
            try:
                # WebDriver waits up to 10 seconds before throwing a TimeoutException
                # unless it finds the element (search box) to return within 10 seconds.
                search_box = WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.NAME, 'q'))
                )
                if search_box:
                    sleep(2)
                    # send keyword to search box
                    self.driver.find_element_by_name('q').send_keys(self.kw, Keys.ENTER)

                    # WebDriver waits up to 10 seconds before throwing a TimeoutException
                    # unless it finds the element (links in results) to return within 10 seconds.
                    links = WebDriverWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.ID, 'links'))
                    )
                    if links:
                        # scroll down page
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sleep(2)  # delay

                        # Finds multiple elements by css selector.
                        if self.driver.find_elements_by_css_selector(MORE_RESULTS):
                            # Clicks the element
                            self.driver.find_elements_by_css_selector(MORE_RESULTS)[0].click()
                            sleep(2)  # delay

                        # Gets the source of the current page, and add links from
                        # search results to a text file
                        append_links_to_file(self.driver.page_source)

            except (NoSuchElementException or WebDriverException) as e:
                self.driver.quit()
                sys.exit(e)

            self.driver.quit()
        else:
            sys.exit("couldn't use the WebDriver")


def append_links_to_file(htm):
    """
    add links from search results (inside given HTML Source) to a text file
    :param htm: HTML Source from a web page (str)
    :return:
    """
    if htm:
        # creates new instance of BeautifulSoup obj with markup to be parsed
        soup = BeautifulSoup(htm, features='html.parser')
        if soup:
            links_section = soup.find(id="links")  # find links section from search results
            if links_section:
                # Extracts a list of Tag objects that match the given criteria.
                a_tags = links_section.find_all('a', class_=re.compile("^result__a"))
                print(a_tags)
                if a_tags:
                    # Open file and return a stream
                    with open(os.path.join(DESKTOP_PATH, "result_links.txt"), "a") as my_file:
                        for a in a_tags:
                            # check whether <a> tag has href and starts with https (HTTPS)
                            if a.has_attr('href') and str(a['href']).startswith('https://'):
                                my_file.write(str(a['href'])+"\n")  # Write string to stream.
                    my_file.close()


if __name__ == '__main__':
    keyword = None
    driver_type = None
    if len(sys.argv) > 1:
        # Object for parsing command line strings into Python objects.
        parser = argparse.ArgumentParser()
        # Adding argument actions
        parser.add_argument("-kw", "--KEYWORD", dest="keyword", type=str,
                            help="Enter a keyword to search with 'duckduckgo' search engine")
        parser.add_argument("-wd", "--WEBDRIVER", dest="driver_type", type=str,
                            help="Enter a browser to simulate (chrome/firefox/edge)")
        args = parser.parse_args()  # Command line argument parsing methods
        keyword = args.keyword  # given keyword (command line arg)
        driver_type = args.driver_type  # driver type (command line arg)

        # Creates new instance of SearchKeywordWithSelenium - simulates chrome/firefox/edge browser
        kw_search = SearchWithSelenium(kw=keyword, driver_name=driver_type)
        # search a keyword with duckduckgo and append links from search results to a text file
        kw_search.search_on_duckduckgo()
