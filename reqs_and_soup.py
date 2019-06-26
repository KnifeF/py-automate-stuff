#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using Requests HTTP Library and BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup

__email__ = "knifef@protonmail.com"

BASE_URL = "http://docs.python-requests.org/en/master/"

req = requests.get(BASE_URL)  # Sends a GET request.

# Integer Code of responded HTTP Status 200 - Standard response for successful HTTP requests.
if req.status_code == 200:
    response_content = req.content  # Content of the response (web page source)
    soup = BeautifulSoup(response_content, 'html.parser')  # new BeautifulSoup Obj

    # Get all child strings, concatenated using the given separator.
    web_page_text = soup.getText()
    print("text from web page:\n***************\n", web_page_text)

    print("links from web page:\n***************\n")
    c = 1
    # Extracts a list of Tag objects that match the given criteria
    for a_tag in soup.find_all('a'):
        if a_tag.has_attr('href') and a_tag.string:  # check if tag has attribute 'href'
            # Returns the value of the 'key' attribute for the tag
            link = a_tag.get('href')
            # Get string within this tag
            title = a_tag.string.strip()

            print("link %d --> " % c, link)
            print("title %d -->" % c, title, "\n*****************\n")
            c += 1
