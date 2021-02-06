#!/usr/bin/env python

import re
import sys
import string
import urllib2
import socket
from HTMLParser import HTMLParser
from collections import Counter

""" Sets rules for how to parse html tags and actual content in website """
class FreqHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_tags = []
        self.attrs = []
        self.end_tags = []
        self.data = []
        self.etc_data = []
        self.reset()
    def handle_starttag(self, tag, attrs):
        self.start_tags.append(tag)
        self.attrs.append(attrs)
    def handle_endtag(self, tag):
        self.end_tags.append(tag)
    def handle_data(self, data):
        self.data.append(data)
    def handle_comment(self, data):
        self.etc_data.append(data)
    def clean(self):
        self.start_tags = []
        self.attrs = []
        self.end_tags = []
        self.data = []

# Find the top n (count) frequent used words
def find_most_frequent(word_array, count):
    print ("The %s most frequent used words on the page are:") % count
    freqs = Counter(word_array).most_common(int (count))
    for each in freqs:
        print each

# Remove punctions from any words strings
def replace_punct(word, punct):
    for sym in punct:
        if word.endswith(sym):
            word = word.replace(sym, "")
    return word

# Parse each valid word from the website address page
def parse_strings_from_data(data): # another arg here for #
    # Use regex to seperate and find all valid strings
    alpha_strings = re.compile('[a-z]+', re.IGNORECASE)
    # Punctioation marks
    punct = ('.', '?', ',', '!', ':', ';')
    wordList = []

    # Search through data and find real words
    for str_data in data:
        # Use regex to check strings for letters
        if alpha_strings.match(str_data):
            split_string = string.split(str_data)
            # Iterate again to catch seperate only strings that contain words
            for strings in split_string:
                # Split real words away from punctiations
                if strings.endswith(punct):
                    strings = replace_punct(strings, punct)
                # Ensure that only  alpha characters are stored for the array
                if strings.isalpha():
                    wordList.append(string.lower(strings)) # Force lowercase
    return wordList

# Takes the site url and html_parser object as a parameters
def parse_html_tags(site, html_parser):
    # Feed one line at a time to run html parsing rules on.
    for line in site:
        html_parser.feed(line)

if __name__ == '__main__':
    # Take input of URL
    url = sys.argv[1]
    num = sys.argv[2]
    print url
    # Instantiate FreqHTMLParser to handle parsing rules
    html_parser = FreqHTMLParser()
    # Connect to url web page
    website = urllib2.urlopen(url)

    # Parse and store data from the site
    parse_html_tags(website, html_parser)
    start_tags = html_parser.start_tags
    end_tags = html_parser.end_tags
    attributes = html_parser.attrs
    data = html_parser.data

    # Parse current data for valid strings
    words = parse_strings_from_data(data)

    # Find most used words on webpage
    find_most_frequent(words, num)
    html_parser.clean()

    """ Notes for improvement:
    No real error checking as of right now. Could use some exception
    and error handling. Examples, Input Handling, timeout errors

    Currently not able to parse contraction words appropriately
    """
