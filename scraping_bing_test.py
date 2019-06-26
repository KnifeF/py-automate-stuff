#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This simple script searches a keyword with 'Bing', and parses the first ten URLs from search results.

The script is using - Selenium Automation Tool (WebDriver) to search terms with 'Bing',
'Beautifulsoup'&'re' to parse results from HTMLs, and 'codecs' to save the results to a CSV file.
"""

import codecs
import re
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

__author__ = "KnifeF"
__license__ = "MIT"
__email__ = "knifef@protonmail.com"

# the path to 'chromedriver' (String)
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
WITHOUT_EXTENSIONS = "--disable-extensions"  # argument to add for the Webdriver (without extensions)
INCOGNITO = "--incognito"  # argument to add for the Webdriver (incognito mode)
BING_URL = r"https://www.bing.com/"  # Bing's URL
NO_RESULTS = r'No results found for'  # appears when there are no results for a search term
SEARCH_HELP = "Web Search Help"  # appears when there are no results for a search term
LIMIT = 10  # limit to results on the first page from search results.


def save_to_csv(parsed_links, key_word):
    """
    Save the results to a CSV file on Desktop (and the file name will be the keyword).
    :param parsed_links: list of tuples, with the links from search results (list).
    :param key_word: the searched keyword, as the name of the filename (String)
    """

    # Open an encoded file using the given mode and return a wrapped version
    # providing transparent encoding/decoding.
    with codecs.open(os.path.join(os.environ["HOMEPATH"], "DESKTOP", key_word + ".csv"),
                     'w', encoding='utf-8-sig') as out_f:
        for index in parsed_links:  # for loop over a list
            # Write string to stream (with indexes from the current tuple)
            out_f.write(index[0]+', '+index[1]+', '+index[2]+"\n")


def parsing_bing_results(source, key_word):
    """
    Parse the top 10 links from the results and adds them to a list.
    :param source - The web page source with the search results (string)
    :param key_word - Search term (string)
    :return: parsed_data - list of tuples [(count_links, link_url, link_text), ...],
    or None when there are no results for the search term
    """

    # initialize new 'BeautifulSoup' Obj (with Python’s html.parser)
    soup = BeautifulSoup(source, 'html.parser')
    # find the first child of matching tag by the given id
    results = soup.find(id="b_results")

    # checks if there are not results for the search term
    if results.find(text=re.compile(NO_RESULTS)) and results.find(text=re.compile(SEARCH_HELP)):
        print("No Results Found For {}".format(key_word))
        return None

    # find the number of search results for the given search term
    if soup.find(id='b_tween'):
        # Prints the number of search results
        print("Number of search results: {}".format(soup.find(id='b_tween').getText()), "\n\n")

    parsed_data = [("Link_Number", "link_URL", "Link_Name")]  # creates a list with a tuple within
    count_links = 0

    for elem in results:  # for loop over the elements

        # A limit of 10 links to parse.
        if count_links == LIMIT:
            break
        link = elem.find('a')  # find <a> tag
        if link:
            count_links += 1
            print(count_links, "\n")
            print(link.get('href'), "\n")
            print(link.getText(), "\n", "********************************************, ""\n")

            link_url = link.get('href')  # href attribute of <a> tag
            link_text = link.getText()  # the text of the <a> tag
            # append 'count_links', 'link_url' and 'link_text' as a tuple to list
            parsed_data.append((str(count_links), link_url, link_text))

    return parsed_data


def bing_search(driver, key_word):
    """
    Navigate to Bing and search the keyword (search term).
    :param driver - the webdriver is used for web scraping (webdriver.Chrome)
    :param key_word - (search term) string
    """
    # Return whether the given object is an instance of webdriver.Chrome
    if isinstance(driver, webdriver.Chrome):
        # navigate to Bing's url in the current browser session
        driver.get(BING_URL)

        sleep(3)  # Delay execution for a given number of seconds

        search_box = driver.find_elements_by_name('q')  # find the search query box element by it's name ('q')

        if len(search_box) > 0:
            # send keyword to the query box element, and hit ENTER to search the term with Bing
            search_box[0].send_keys(key_word, Keys.ENTER)

            # driver.find_elements_by_name('go').click()


def scraping_process(driver, key_word):
    """
    Manage the scraping process (search, get page's source, parse the links and create a csv file).
    :param driver - the webdriver is used for web scraping (webdriver.Chrome)
    :param key_word - (search term) string
    """
    bing_search(driver, key_word)  # search the keyword with Bing

    sleep(3)  # Delay execution for a given number of seconds

    # Return whether the given object is an instance of webdriver.Chrome
    if isinstance(driver, webdriver.Chrome):
        source = driver.page_source  # Gets the source of the current page

        parsed_links = parsing_bing_results(source, key_word)  # parse the first ten results, and add to a list

        if parsed_links:
            save_to_csv(parsed_links, key_word)  # save the results to a CSV file


def set_chrome_driver():
    """
    Set the webdriver with Chrome options.
    Return Value: driver - the webdriver is used for web scraping (webdriver.Chrome)
    """
    chrome_options = webdriver.ChromeOptions()  # preferences for chrome webdriver
    chrome_options.add_argument(WITHOUT_EXTENSIONS)  # add argument to ChromeOptions (without extensions)
    chrome_options.add_argument(INCOGNITO)  # add argument to ChromeOptions (incognito mode)

    # Creates a new instance of the chrome driver
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)

    return driver


def receive_user_input():
    """
    Receive keyword from user input (search term).
    :return: key_word - (search term) string
    """
    key_word = input("Enter a keyword to search with Bing:\n")
    print(key_word)
    return key_word


def main():
    """
    The main function (runs the wcraper).
    """
    key_word = receive_user_input()  # Receive keyword from user input

    # Creates a new instance of the chrome driver with required preferences/options
    driver = set_chrome_driver()

    if key_word:
        # scrape the first ten results for keyword in Bing, ands save the results to a CSV file
        scraping_process(driver, key_word)


if __name__ == "__main__":
    main()
