#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This simple script searches for elite/anonymous proxies (with SSL) & common Chrome user agents (for computers),
and saves them to text files on desktop.

The script might be useful to extract recent/common user agents & proxy severs (IP:PORT format),
in order to use them for various purposes, including:
1. Web Scraping with bots&crawlers - using proxies, and/or faking user agents, to prevent getting blocked
while scraping websites.
2. Web Testing - use proxies and/or manipulate the user agent (using common UA) on your monitors to test
content meant for other locations, browsers, operating systems, and devices (mobile phones, tablets etc.).

The proxies are taken from 'https://free-proxy-list.net/',
and user agents from 'https://developers.whatismybrowser.com'

The script is using - Selenium WebDriver (Chrome - headless browser) to scrape the data from web,
'Beautifulsoup' to parse results from HTMLs, and 'codecs' to save the results to text files.
"""

import os
import codecs
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

__author__ = "KnifeF"
__license__ = "MIT"
__email__ = "knifef@protonmail.com"


# ****************************************WebDriver Settings / parameters***************************************
WITHOUT_EXTENSIONS = "--disable-extensions"  # disable extensions
PREFERENCES = {'profile.managed_default_content_settings.javascript': 2}  # Disable JavaScript From Browser

CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'chromedriver')  # path to chromedriver

PREFERENCES_PATH = os.path.join(os.environ["HOMEPATH"],
                                r'AppData\Local\Google\Chrome\User Data\Default')  # path to chrome User Data

PROXIES_SITE = "https://free-proxy-list.net/"  # proxies' website URL
USER_AGENTS_SITE = "https://developers.whatismybrowser.com/useragents/explore/"  # user-agents' website URL

# the text of the link contains 'Chrome' (to explore 'Chrome' user agents)
CHROME_LINK = r"//a[text()[contains(.,'Chrome')]]"

# ****************************************Folder paths for saving files*******************************************
DESKTOP_PATH = os.path.join(os.environ["HOMEPATH"], "DESKTOP")


class GetProxiesAndUserAgents:

    def __init__(self):
        """
        creates new instance of ProxiesScraper Object
        """
        self.driver = None  # the WebDriver
        self.set_chrome_driver()  # Creates a new instance of the chrome driver with required parameters
        self.proxies = []  # list of proxies
        self.user_agents = []  # list of user agents

    def set_chrome_driver(self, activate_proxy=False, use_user_agent=False, hide_window=True):
        """
        Set chromedriver to the desirable mode (with options and arguments)
        :param activate_proxy: True - to add proxy as argument in ChromeOptions, or False.
        :param use_user_agent: True - to add user agent argument in ChromeOptions, or False.
        :param hide_window: True - to use headless browser in ChromeOptions,
        or False - to show visible browser window.
        :return:
        """
        # a copy of default supported desired capabilities of chrome browser
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True    # accept all SSL certs by default
        capabilities['acceptInsecureCerts'] = True  # accept Insecure Certs

        options = webdriver.ChromeOptions()  # build options for chrome.
        options.add_argument("--incognito")  # incognito mode in chrome without using 'User Data'
        if hide_window:
            options.add_argument("--headless")  # headless browser
        options.add_argument("--start-fullscreen")  # fullscreen option in chrome
        options.add_experimental_option("prefs", PREFERENCES)  # option that disables JavaScript in chrome
        options.add_argument(WITHOUT_EXTENSIONS)  # disable extensions in chrome

        rnd_proxy = None
        if activate_proxy:
            if self.proxies:
                if len(self.proxies) > 1:
                    rnd_proxy = self.proxies[randint(0, len(self.proxies)-1)]  # random proxy from list
                else:
                    rnd_proxy = self.proxies[0]
                options.add_argument(r'--proxy-server=%s' % rnd_proxy)  # adds proxy as argument of ChromeOptions
                print("Chosen Proxy --> "+rnd_proxy)

        if use_user_agent:
            if self.user_agents and len(self.user_agents) > 1:
                # random user agent from list
                rnd_user_agent = self.user_agents[randint(0, len(self.user_agents)-1)]
                options.add_argument(r'--user-agent="%s"' % rnd_user_agent)
                print("Chosen Chrome user agent --> " + rnd_user_agent)
        sleep(5)

        # creating object (webdriver.Chrome)
        chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options,
                                         desired_capabilities=capabilities)

        if rnd_proxy:
            # Set the amount of time to wait for a page load to complete before throwing an error.
            chrome_driver.set_page_load_timeout(30)
        chrome_driver.delete_all_cookies()  # deletes all stored cookies
        self.driver = chrome_driver

    def destroy_driver(self):
        """
        close the drivers after deleting all cookies, set the WebDriver value to 'None',
        and enable javascript on chrome Preferences.
        :return:
        """
        # close the drivers and set the WebDriver value to 'None'
        if self.driver:
            self.driver.delete_all_cookies()  # delete cookies in the scope of the session
            self.driver.quit()  # Closes the browser and shuts down the ChromeDriver
            self.driver = None  # change value to None
        enable_js_preference()  # fix javascript to be enabled on chrome browser Preferences

    def reopen_driver(self, activate_proxy=False, use_user_agent=False, hide_window=True):
        """
        close and open again the webdriver
        :param activate_proxy: True - to add proxy as argument in ChromeOptions, or False.
        :param use_user_agent: True - to add user agent argument in ChromeOptions, or False.
        :param hide_window: True - to use headless browser in ChromeOptions,
        or False - to show visible browser window.
        :return:
        """
        # open new WebDriver if not opened yet
        self.destroy_driver()  # close webdriver after deleting cookies
        sleep(3)  # delay in seconds

        # sets required options and arguments in 'webdriver.Chrome'
        self.set_chrome_driver(activate_proxy=activate_proxy, use_user_agent=use_user_agent,
                               hide_window=hide_window)

    def scrape_user_agents(self):
        """
        navigate to website that contains user-agents , parse user-agents data
        (by Chrome User Agents on Windows/Linux), add it to user-agents list and save data to a text file
        :return:
        """
        if self.driver:
            self.driver.get(USER_AGENTS_SITE)  # navigates to the web page
            sleep(randint(3, 9))  # random delay

            # Finds multiple elements by xpath
            a_tags = self.driver.find_elements_by_xpath(CHROME_LINK)
            if a_tags:
                a_tags[0].click()  # click on the first element
                sleep(3)  # delay in seconds

                # identify that the Chrome User Agents page appeared
                if ("Chrome User Agents" in self.driver.page_source) \
                        or ("Chrome user agents" in self.driver.page_source):

                    page_num = 1
                    stop = False
                    while page_num < 12 and not stop:
                        source = self.driver.page_source  # Gets the source of the current page
                        current_url = self.driver.current_url  # Gets the url of the current page
                        soup = BeautifulSoup(source, 'html.parser')  # build BeautifulSoup Obj (with html source)

                        print("page --> "+str(page_num))

                        # find first element by tag 'table' (should include table of user agents)
                        user_agents_tbl = soup.find("table")
                        if user_agents_tbl:
                            table_body = user_agents_tbl.find("tbody")  # find body content in HTML table
                            if table_body:
                                # Find all <tr> tags. The <tr> tag defines a row in an HTML table.
                                #  A <tr> element contains one or more <th> or <td> elements.
                                for tr in table_body.findAll('tr'):
                                    tr_text = tr.getText()  # all text inside the <tr> element

                                    # check for a common 'Chrome user agent' (for a computer)
                                    if tr_text and ("Chrome" in tr_text) and ("Computer" in tr_text) \
                                            and ("common" in tr_text.lower()):
                                        # find td with class 'useragent'
                                        user_agent_td = tr.find('td', class_="useragent")
                                        if user_agent_td:
                                            link = user_agent_td.find("a", text=True)
                                            if link:
                                                a_text = link.getText()  # link text
                                                self.user_agents.append(a_text)

                                # find <a> tags in <div id='pagination'>, that their text contains '>'
                                next_page = self.driver.find_elements_by_xpath(r"//div[@id='pagination']//"
                                                                               r"a[text()[contains(.,'>')]]")
                                if next_page:
                                    next_page[0].click()  # click on link to next page '>'
                                    page_num += 1
                                    sleep(randint(3, 5))  # random delay in seconds
                                    old_url = current_url
                                    # check if the URL is the same, after an attempt to move to the next page
                                    if old_url == self.driver.current_url:
                                        stop = True
                                else:
                                    stop = True
                        if page_num == 0:
                            stop = True
            if self.user_agents:
                # save the user-agents to a Text file on Desktop (called 'common_user_agents')
                data_to_file(self.user_agents, 'common_user_agents')
                print("finished scraping user agents")
            self.destroy_driver()

    def scrape_proxies(self):
        """
        navigate to website that contains proxies (IPs), parse proxy data,
        add it to proxy list, and save data to a text file
        :return:
        """
        if self.driver:
            self.driver.get(PROXIES_SITE)  # navigates to the web page
            sleep(randint(3, 9))  # random delay
            source = self.driver.page_source  # Gets the source of the current page
            soup = BeautifulSoup(source, 'html.parser')  # build BeautifulSoup Obj (with html source)

            # find element by tag and id (should include table of proxies)
            proxy_tbl = soup.find("table", id="proxylisttable")

            if proxy_tbl:
                # find body content in HTML table
                table_body = proxy_tbl.find("tbody")

                if table_body:
                    # Find all <tr> tags. The <tr> tag defines a row in an HTML table.
                    # A <tr> element contains one or more <th> or <td> elements.
                    for tr in table_body.findAll('tr'):
                        if len(list(tr.children)) >= 7:  # 7 or more children to the element
                            res = ""
                            for td in tr.findAll('td'):  # loop over <td> (inside <tr>)
                                td_text = td.getText()  # the text of the child
                                if td_text:
                                    res += td_text+", "
                            if res:
                                print(res)
                                self.proxies.append(res)  # append text to proxy list
                                # res = ""

                    good_proxies = []
                    if self.proxies:
                        print("\n\n\n")
                        for index in range(len(self.proxies)):

                            # the proxy is from type 'elite' or 'anonymous', and 'yes' indicates
                            # that the proxy works with 'https' (SSL) or works on google
                            if ("elite proxy" in self.proxies[index] or "anonymous" in self.proxies[index]) \
                                    and ("yes" in self.proxies[index]):

                                split_proxy_str = self.proxies[index].split(", ")  # split string by commas

                                print("IP&PORT --> " + split_proxy_str[0] + ":"
                                      + split_proxy_str[1] + " | COUNTRY --> " + split_proxy_str[3])

                                # append the proxy to the list as string (proxy:port)
                                good_proxies.append(split_proxy_str[0]+":"+split_proxy_str[1])

                    self.proxies = None
                    if good_proxies:  # found good proxies
                        self.proxies = good_proxies
                        # save the proxies to a Text file on Desktop (called 'recent_proxies')
                        data_to_file(self.proxies, 'recent_proxies')
                        print("finished scraping proxies")
                    else:
                        print("couldn't get good proxies (elite proxies on port 8080)")
                    self.destroy_driver()


def data_to_file(data_lst, file_name):
        """
        save data from list to a text file on desktop
        :param data_lst: list with data
        :param file_name: the name for output file
        :return:
        """
        if file_name and data_lst:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            with codecs.open(os.path.join(DESKTOP_PATH, file_name),
                             'w', encoding='utf-8') as out_f:
                for i in data_lst:
                    out_f.write(str(i)+"\n")
            out_f.close()


def enable_js_preference():
    """
    fixes problem that enforces javascript to be disabled on browser.
    remove from file a preference that disable javascript in chrome as default ("javascript":2).
    :return:
    """
    f = open(os.path.join(PREFERENCES_PATH, 'Preferences'), "r+")  # open file on read mode
    d = f.readlines()  # Read and return a list of lines from the stream
    f.seek(0)  # Change stream position - to the start of stream (the default)
    for index in d:
        if r',"managed_default_content_settings":{"javascript":2}' in index:
            # Return a copy of string with all occurrences of substring old replaced by new.
            # remove from line a preference that disable javascript in chrome as default ("javascript":2)
            f.write(index.replace(r',"managed_default_content_settings":{"javascript":2}', ''))
        else:
            f.write(index)  # write the line without changes
    f.truncate()  # Truncate file to size bytes.
    f.close()  # Flush and close the IO object.


def main():
    """
    The main function
    :return:
    """
    sleep(5)
    scraper = GetProxiesAndUserAgents()  # build new 'GetProxiesAndUserAgents' object
    scraper.scrape_proxies()  # trying to find available proxies on 'https://free-proxy-list.net/'
    scraper.reopen_driver()  # close and open again the webdriver

    # trying to find available chrome user agents on
    # 'https://developers.whatismybrowser.com/useragents/explore/'
    scraper.scrape_user_agents()

    scraper.destroy_driver()  # destroy the webdriver

if __name__ == '__main__':
    main()
