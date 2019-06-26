#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using urllib3 (powerful, sanity-friendly HTTP client) library and BeautifulSoup.
"""

import urllib3
import certifi
from bs4 import BeautifulSoup

__email__ = "knifef@protonmail.com"

BASE_URL = "https://urllib3.readthedocs.io/en/latest/"


# Allows for arbitrary requests while transparently keeping track of necessary connection pools for you.
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
# Make a 'GET' HTTP request
req = http.request('GET', BASE_URL)

# Integer Code of responded HTTP Status 200 - Standard response for successful HTTP requests.
if req.status == 200:
    req_data = req.data  # The data attribute of the response (web page source)

    soup = BeautifulSoup(req_data, 'html.parser')  # new BeautifulSoup Obj

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
