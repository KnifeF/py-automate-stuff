#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Using robobrowser library (Robotic web browser. Represents HTTP requests and 
responses using the requests library and parsed HTML using BeautifulSoup)

The script scrapes artists' data on https://www.lyrics.com/, and stores text (bio and albums) 
from an HTML page source of each artist's page in file (text&csv files)."""

import sys
import os
import codecs
import argparse
import pandas as pd
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from time import sleep

__email__ = "knifef@protonmail.com"

BASE_URL = "https://www.lyrics.com/"
ARTISTS_PATH = os.path.join(os.environ["HOMEPATH"], "DESKTOP", "artists")


def scrape_bio_and_albums(keywords):
    """
    scrapes artists' data on https://www.lyrics.com/, and stores text (bio and albums)
    from an HTML page source of each artist's page in file (text&csv files).
    :param keywords: list of keywords that should represent artists' names (list)
    :return:
    """
    if keywords and isinstance(keywords, list):

        # builds new object of RoboBrowser with given params
        browser = RoboBrowser(parser='html.parser',
                              user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                         '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                              history=True, timeout=10)
        # Open a URL (using 'RoboBrowser' library).
        browser.open(BASE_URL)

        for keyword in keywords:
            if keyword and len(keyword) > 1:

                # get browser url (should be 'old' after searching a term - if browser goes to new url)
                old_url = browser.url

                # trying to search keyword on 'lyrics.com' (using RoboBrowser's methods to handle forms)
                form = browser.get_form(id='search-frm')  # Find form by ID 'search-frm'
                form['st'].value = keyword  # sets query value 'st' with given keyword
                browser.submit_form(form)  # Submit a form - to search given keyword

                # check if the url is changed (after searching a keyword)
                if old_url != browser.url:

                    # select required <a> tags, using CSS Selectors (see on BeautifulSoup's documentation)
                    a_tags = browser.select('body p[class~=serp-flat-list] a[href^=artist/]')

                    if a_tags:
                        # browser.follow_link(a_tags[0])

                        # builds base url with href - to open required url using 'open()' method,
                        # and avoid including the "/lyrics/" part in url, when using 'follow_link()' method
                        first_artist_url = a_tags[0]['href'].replace("artist", BASE_URL+"artist")

                        # Open URL (should get url of the first suggested artist's page in results)
                        browser.open(first_artist_url)

                        # parse response content (bs4 obj), using HTML parser specified by the browser
                        soup = browser.parsed

                        if soup:
                            artist_bio_tag = soup.find(class_='artist-bio')  # find tag by class
                            if artist_bio_tag:
                                # save parsed text (artist bio) from page source to a text file
                                save_source(keyword+" - bio", artist_bio_tag.get_text(),
                                            dir_path=os.path.join(ARTISTS_PATH, keyword))
                                # parse albums&songs from html tables, and save the data to a csv file
                                albums_to_csv(soup, keyword+" - albums", dir_path=os.path.join(ARTISTS_PATH, keyword))

                        browser.back()  # Go back in browser history.
                    browser.back()  # Go back in browser history.


def save_source(file_name, res, dir_path=ARTISTS_PATH):
        """
        save page source data to a text file
        :param file_name: the name for output file
        :param res: string to write to a file
        :param dir_path: path to dir to save file
        :return:
        """
        if dir_path:
            if create_dir(dir_path):  # Test whether a path exists, and create dirs in path (if not exist)
                sleep(1)  # delay
                if file_name and res:
                    if not file_name.endswith(".txt"):
                        file_name += ".txt"
                    with codecs.open(os.path.join(dir_path, file_name),
                                     'w', encoding='utf-8') as out_f:
                        out_f.write(res)
                    out_f.close()


def albums_to_csv(soup_obj, file_name, dir_path=ARTISTS_PATH):
    """
    trying to parse albums&songs from html tables, and save the data to a csv file (using pandas)
    :param soup_obj: Beautifulsoup obj
    :param file_name: the name for output file
    :param dir_path: path to dir to save the file
    :return:
    """
    if soup_obj and isinstance(soup_obj, BeautifulSoup) and dir_path:

        albums_elems = soup_obj.find_all(class_='clearfix')  # find tags by class
        if albums_elems:
            raw_data = {}
            for album_elem in albums_elems:

                album_title_elem = album_elem.find(class_='artist-album-label')  # find tag by class
                if album_title_elem:
                    album_title = album_title_elem.get_text()  # album title (str)
                    if album_title:
                        # initialize dict key (album's name) with an empty list
                        raw_data[album_title] = []
                        # select tr tags from table's body
                        song_elems = album_elem.select('table tbody tr')
                        for tr in song_elems:
                            if tr:
                                song_name_elem = tr.find('td')  # find first td elems
                                if song_name_elem:
                                    song_name = song_name_elem.get_text()  # text within tag
                                    if song_name:
                                        raw_data[album_title].append(song_name)  # append to list

            if raw_data:
                # new DataFrame from dict, and Transpose index and columns.
                df = pd.DataFrame.from_dict(raw_data, orient='index').transpose()

                if not df.empty:  # check if DataFrame is not empty

                    if file_name.endswith(".csv"):  # str ends with ".csv"
                        # Return a copy of the string with all occurrences of substring old replaced by new
                        file_name = file_name.replace(".csv", "")

                    # Test whether a path exists, and create dirs in path (if not exist)
                    if create_dir(os.path.join(dir_path)):
                        sleep(1)  # delay
                        # save Pandas DataFrame to a CSV file
                        df.to_csv(os.path.join(dir_path, file_name+".csv"), sep='\t',
                                  encoding='utf-8-sig', index=False)


def create_dir(path):
    """
    Test whether a path exists, and create dirs in path (if not exist).
    :param path: path to check whether it exists or not.
    :return: boolean - True if path exists, or False
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except OSError:
        print("OS Error")
        return False


if __name__ == '__main__':

    given_key_words = None
    if len(sys.argv) > 1:
        # Object for parsing command line strings into Python objects.
        parser = argparse.ArgumentParser()
        # Adding argument actions
        parser.add_argument("-kw", "--KEYWORD", dest="given_key_words", type=str, nargs='*',
                            help="Enter keywords (artists), to search them on 'https://www.lyrics.com/'")
        args = parser.parse_args()  # Command line argument parsing methods
        given_key_words = args.given_key_words
    else:
        given_key_words = ['Lady Gaga', 'Michael Jackson']

    # scrapes artists' data on https://www.lyrics.com/
    scrape_bio_and_albums(given_key_words)
