#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This simple script searches for facebook uids of given facebook usernames, using different proxy servers.

The script might be useful for Reconnaissance/OSINT, in case that there is a need to map/research
a bunch of fb profiles, and get their uids (useful when running some queries).

The proxies are taken from 'https://free-proxy-list.net/'
The script is using - Selenium Automation Tool (WebDriver) to scrape the web,
'Beautifulsoup'&'re' to parse results from HTMLs, and 'codecs' to save the results to a file.
"""

import re
import os
import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from time import sleep
from bs4 import BeautifulSoup
from random import randint

__author__ = "KnifeF"
__license__ = "MIT"
__email__ = "knifef@protonmail.com"


# ****************************************WebDriver Settings / parameters***************************************
WITHOUT_EXTENSIONS = "--disable-extensions"
PREFERENCES = {'profile.managed_default_content_settings.javascript': 2}  # Disable JavaScript From Browser
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
PREFERENCES_PATH = os.path.join(os.environ["HOMEPATH"], r'AppData\Local\Google\Chrome\User Data\Default')
PROXIES_SITE = "https://free-proxy-list.net/"  # proxies' website URL
FIND_FBID = "https://findmyfbid.com/"  # URL of a website that is used to convert fb usernames to uids

# ****************************************Folder paths for saving files*******************************************
DESKTOP_PATH = os.path.join(os.environ["HOMEPATH"], "DESKTOP")


class FbidScraper:

    def __init__(self, f_path):
        """
        creates new instance of FbidScraper Object
        :param f_path: path to a file (string)
        """
        # build the scraper object
        self.facebook_users = []  # list of facebook usernames
        self.facebook_uids = []  # list of facebook uids
        self.driver = None  # the WebDriver
        self.proxies = []  # list of proxies
        # filter users from text file, and fill data in 'self.facebook_users' & 'self.facebook_uids'
        self.filter_users(f_path)

    def set_chrome_driver(self, activate_proxy=False):
        """
        Set chromedriver to the desirable mode (with options and arguments)
        :param activate_proxy: True - to add proxy as argument in ChromeOptions, or False.
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # incognito mode in chrome without using 'User Data'
        options.add_experimental_option("prefs", PREFERENCES)  # option that disables JavaScript in chrome
        options.add_argument(WITHOUT_EXTENSIONS)  # disable extensions in chrome

        if activate_proxy:
            if self.proxies:
                if len(self.proxies) > 1:
                    rnd_proxy = self.proxies[randint(0, len(self.proxies)-1)]  # random proxy from list
                else:
                    rnd_proxy = self.proxies[0]
                options.add_argument('--proxy-server=%s' % rnd_proxy)  # adds proxy as argument of ChromeOptions
                print("Chosen Proxy --> "+rnd_proxy)
        sleep(5)

        # creating object (webdriver.Chrome)
        chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)
        chrome_driver.maximize_window()  # maximize window's size of the browser ('webdriver')
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
            self.driver.delete_all_cookies()
            self.driver.close()  # close WebDriver
            self.driver = None  # change value to None
        enable_js_preference()  # fix javascript to be enabled on chrome browser Preferences

    def reopen_driver(self, activate_proxy=False):
        """
        close and open again the webdriver
        :param activate_proxy: True - to add proxy as argument in ChromeOptions, or False.
        :return:
        """
        # open new WebDriver if not opened yet
        self.destroy_driver()
        sleep(randint(3, 9))

        # sets required options and arguments in 'webdriver.Chrome'
        self.set_chrome_driver(activate_proxy=activate_proxy)

    def extract_proxies(self):
        """
        navigate to website that contains proxies (IPs), parse proxy data, and add it to proxy list
        :return:
        """
        if self.driver and self.facebook_users:
            self.driver.get(PROXIES_SITE)
            sleep(randint(5, 15))
            source = self.driver.page_source  # Gets the source of the current page

            soup = BeautifulSoup(source, 'html.parser')  # new BeautifulSoup Obj
            proxy_tbl = soup.find(id="proxylisttable")  # find element by id
            if proxy_tbl:

                # Find all <tr> tags. The <tr> tag defines a row in an HTML table.
                # A <tr> element contains one or more <th> or <td> elements.
                for tr in proxy_tbl.findAll('tr'):
                    if len(list(tr.children)) >= 7:  # 7 or more children to the element
                        res = ""
                        for td in tr.children:  # loop over <tr> children (<td>)
                            td_text = td.getText()  # the text of the child
                            if td_text:
                                res += td_text+", "
                        if res:
                            self.proxies.append(res)  # append text to proxy list
                            # res = ""

                good_proxies = []
                if self.proxies:
                    for index in range(len(self.proxies)):

                        # the proxy is from type 'elite' or 'anonymous', the port is '8080',
                        # and 'yes' indicates that the proxy works with 'https' or works on google
                        if ("elite proxy" in self.proxies[index] or "anonymous" in self.proxies[index]) \
                                and ("8080" in self.proxies[index]) \
                                and ("yes" in self.proxies[index]):

                            split_proxy_str = self.proxies[index].split(", ")  # split string by commas
                            print(split_proxy_str[0]+":"+split_proxy_str[1]+" --> "+split_proxy_str[3])
                            # append the proxy to the list as string (proxy:port)
                            good_proxies.append(split_proxy_str[0]+":"+split_proxy_str[1])

                self.proxies = None
                if good_proxies:  # found good proxies
                    self.proxies = good_proxies
                else:
                    print("couldn't get good proxies (elite proxies on port 8080)")
                self.driver.delete_all_cookies()  # delete cookies
                self.destroy_driver()  # destroy the webdriver

    def filter_users(self, f_path):
        """
        filter profiles' usernames from text file. append the ids to facebook_uids list
        :param f_path: path to a file (string)
        :return:
        """

        # users_file = os.path.join(DESKTOP_PATH, 'users_to_check.txt')
        self.facebook_users = text_from_file(f_path)
        if self.facebook_users:
            print(self.facebook_users)
            count = len(self.facebook_users)
            index = 0
            while index < count:
                fb_user = self.facebook_users[index]
                if fb_user:
                    fb_user = self.facebook_users[index].replace(" ", "")

                    # check is fb_user does not contain a proper username
                    if (not fb_user) or ("profile.php?id=" in fb_user) or (fb_user.isdigit()):
                        if fb_user.isdigit():  # the string is from digits only
                            self.facebook_uids.append(fb_user)

                        elif "profile.php?id=" in fb_user:  # a part from URL that is already includes the uid
                            tmp_uid = fb_user.split("profile.php?id=")[1]
                            if "&" in tmp_uid:
                                tmp_uid = tmp_uid.split("&")[0]
                            elif "?" in tmp_uid:
                                tmp_uid = tmp_uid.split("?")[0]
                            self.facebook_uids.append(tmp_uid)
                        self.facebook_users.pop(index)  # pop index from list
                        count -= 1
                        index -= 1
                    else:
                        if "facebook.com/" in fb_user:  # given username might be within a facebook url

                            # a list of the words in the string, using sep as the delimiter string
                            split_address = fb_user.split("facebook.com/")
                            fb_user = split_address[1]  # index 1 of the list

                            # all occurrences of substring old replaced by new
                            fb_user.replace("ref=br_rs", "")
                            if "/" in fb_user:
                                fb_user = fb_user.split("/")[0]
                            elif "?" in fb_user:
                                fb_user = fb_user.split("?")[0]
                            elif "&" in fb_user:
                                fb_user = fb_user.split("&")[0]
                        self.facebook_users[index] = fb_user
                else:
                    self.facebook_users.pop(index)  # pop index from list
                    index -= 1
                index += 1

    def uids_from_users(self):
        """
        scrape ids of facebook users (convert username to uid through "findmyfbid" website),
        and sometimes change proxies (to stay more anonymous)
        :return:
        """

        # check if there are existing proxies and facebook usernames
        if self.proxies and self.facebook_users:

            proxy_worked = self.till_proxy_work_loop()  # loop till the proxy will work
            if proxy_worked:  # found proxy that works
                sleep(randint(7, 14))
                count = 0

                for index in self.facebook_users:
                    proxy_worked = True
                    if (count % 10 == 0) and (count != 0):  # count divides by 10
                        # trying to change proxy - loop till the proxy will work
                        proxy_worked = self.till_proxy_work_loop()
                    if proxy_worked:
                        sleep(randint(8, 14))
                        self.scrape_find_my_fbid(index)  # scrape facebook uids
                        count += 1
                self.destroy_driver()  # destroy the webdriver

    def till_proxy_work_loop(self):
        """
        reopens WebDriver from random proxy servers in a loop, till good connection with "findmyfbid" website.
        :return:
        """
        proxy_worked = False
        count = 0
        while count < 15 and not proxy_worked:
            self.reopen_driver(activate_proxy=True)  # close and open the webdriver
            proxy_worked = self.is_proxy_works()  # the proxy works
            count += 1
        return proxy_worked

    def is_proxy_works(self):
        """
         try to get "https://findmyfbid.com/" website, and find that it appears correctly.
        :return:
        """

        try:
            if self.driver:
                self.driver.get(FIND_FBID)  # navigates to the web page
                sleep(randint(3, 6))
                current_source = self.driver.page_source  # Gets the source of the current page

                # indicates that the proxy connection works (the string should appear on the web page)
                if "Find your Facebook ID" in current_source:
                    return True
                else:
                    return False
        except WebDriverException:
            print("WebDriverException")
            pass
        return False

    def scrape_find_my_fbid(self, user):
        """
        takes facebook username and convert it to facebook uid, through "https://findmyfbid.com/"
        enter the username as input, press enter, and parse the uid from result's page source.
        :param user: input username to convert
        :return:
        """

        # Finds a list of elements within this element's children by name
        url_elems = self.driver.find_elements_by_name("url")
        if url_elems:
            # click on the first element, by the name "url" (query search box) - from the list
            url_elems[0].click()
            sleep(1)
            url_elems[0].clear()  # clear the search box
            sleep(1)
            url_elems[0].send_keys(user)  # send the username to the search box
            sleep(1)
            url_elems[0].send_keys(Keys.ENTER)  # hit ENTER to search for the uid of the current username
            sleep(randint(8, 16))
            current_source = self.driver.page_source  # Gets the source of the current page
            if r'{"id":' in current_source:
                # find a result with the uid (in page source)
                uid_tags = re.findall(r'\{"id":[^>]+\}', current_source)
                if uid_tags:
                    # using replace method to remove unwanted occurrences from the string
                    uid = uid_tags[0].replace(r'{"id":', '').replace('}', '').replace(' ', '')
                    if len(uid) > 0 and uid.isdigit():
                        self.facebook_uids.append(uid)  # append uid to list
                        sleep(3)
            sleep(randint(3, 6))
            self.driver.execute_script("window.history.go(-1)")  # going back to previous page


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


def text_from_file(file_name):
    """
    :param file_name: path to a file (string)
    :return: lines from the given file (list)
    """
    res = []
    if os.path.exists(file_name) and os.path.isfile(file_name):  # file exists and is a regular file
        # open file by given path
        with codecs.open(file_name, 'r', encoding='utf-8') as this_file:
            for line in this_file.readlines():
                # remove end of line occurrences, and append line to list
                res.append(line.replace('\n', '').replace('\r', ''))
        this_file.close()
    return res


def receive_user_input():
    """
    Receive input from user (path to a file)
    :return: input from user
    """
    print(r'C:\Users\UsrInspiron133\Desktop\users_to_check.txt')
    key_word = input("Enter file path, like the example above:\n")
    return key_word


def main():
    """
    The main function
    :return:
    """
    file_path = receive_user_input()  # receive file path from user
    scraper = FbidScraper(file_path)  # build new FbidScraper object

    if scraper.facebook_users:  # check if there are facebook users to search for their uids

        # Creates a new instance of the chrome driver with required parameters
        scraper.set_chrome_driver()

        # trying to find available proxies on 'https://free-proxy-list.net/'
        scraper.extract_proxies()
        sleep(3)

        if scraper.proxies:  # found proxies on 'https://free-proxy-list.net/'
            sleep(2)
            scraper.uids_from_users()  # scrape uids from the given usernames

            if scraper.facebook_uids:  # found uids
                # save the uids to a Text file on Desktop (called 'facebook_uids')
                with codecs.open(os.path.join(DESKTOP_PATH, "facebook_uids.txt"), 'w', encoding='utf-8') as out_f:
                    for i in scraper.facebook_uids:
                        out_f.write(str(i)+"\n")
                out_f.close()


if __name__ == '__main__':
    main()
