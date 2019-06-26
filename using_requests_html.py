#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using Requests-HTML Library (HTML Parsing for Humans)
"""

from requests_html import HTML, HTMLSession

# A consumable session, for cookie persistence and connection pooling, amongst other things.
session = HTMLSession()

# Sends a GET request
r = session.get('https://html.python-requests.org/')

# Integer Code of responded HTTP Status 200 - Standard response for successful HTTP requests.
if r.status_code == 200:
    # Convert incoming unicode HTML into bytes
    html = HTML(html=r.content)
    if html:
        # All found links on page, in absolute form
        print(html.absolute_links, "\n\n")

        body = html.find(selector='body', first=True)  # Given a CSS Selector, returns an Element
        print(body.full_text)  # The full text content of the Element
