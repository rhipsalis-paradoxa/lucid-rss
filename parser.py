import urllib.request
import re

import lucid.util as util

import lxml.html as html
import lxml.html.soupparser as soup
from lxml import etree


def xpaths_from_template(template):
    try:
        root = html.fragment_fromstring(template)
    except etree.ParserError:
        return None
    else:
        tree = etree.ElementTree(root)
        xpaths = []
        # traverse the template, saving xpath to any item marked with a $
        for element in root.iter():
            path = tree.getpath(element)
            if element.text == '$':
                xpaths.append('/' + path)
        return xpaths


def extract_articles(feedname, xpaths):
    # Use BeautifulSoup to parse cached HTML document from the feed's
    # target URL.  BeautifulSoup is necessary because it handles
    # broken HTML better than LXML.
    try:
        root = soup.parse(util.feed_html_path(feedname))
    except etree.ParserError:
        return None
    else:
        # Extract the text matching each of the provided xpaths.
        sections = []
        for x in xpaths:
            sections.append([e.text for e in root.xpath(x)])
        # Zip matches together into groups; since the xpaths specify
        # different parts of an article overview, associating the matches
        # together by index should put parts of a corresponding article in
        # the same group.
        return list(zip(*sections))


def fmt_article(template, article):
    # index an element of the article using a matched integer from a
    # Match object.
    def index_element(m):
        i = int(m.group(1))
        # don't try to replace if index is invald
        if i < len(article):
            return article[i]
        else:
            return f"${i}"

    return re.sub(r'\$([0-9]+)', index_element, template)
