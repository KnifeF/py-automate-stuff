#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using urllib.request (a urllib module for opening and reading URLs).
"""

import sys
import re
import socket
from urllib.request import Request, urlopen
from urllib.error import URLError

__email__ = "knifef@protonmail.com"

BASE_URL = "https://docs.python.org/3/library/urllib.html"

if __name__ == '__main__':

    # timeout in seconds
    timeout = 10

    # Set the default timeout in seconds (float) for new socket objects
    socket.setdefaulttimeout(timeout)

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }

    # An extensible library for opening URLs using a variety of protocols
    req = Request(BASE_URL, headers=headers)

    try:
        # Open the URL url, which can be either a string or a Request object,
        # and should use default timeout we have set in the socket module
        response = urlopen(req)
        # a `bytes` object (should contain the HTML source)
        htm = response.read()
        if htm:
            # Return a list of all non-overlapping matches in the string
            href_attrs = re.findall(r'href=[\'"]?([^\'" >]+)', str(htm))
            print(href_attrs)

    except URLError as e:  # The base exception class raised by urllib
        if hasattr(e, 'reason'):
            sys.exit('We failed to reach a server.\nReason: %s' % e.reason)
        elif hasattr(e, 'code'):
            sys.exit('The server could not fulfill the request.\nError code: %s' % e.code)
