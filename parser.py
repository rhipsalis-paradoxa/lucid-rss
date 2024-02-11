import lxml.html as html
from lxml import etree
import urllib.request


def xpaths_from_template(template):
    root = html.fragment_fromstring(template)
    tree = etree.ElementTree(root)
    xpaths = []
    # traverse the template, saving xpath to any item marked with a $
    for element in root.iter():
        path = tree.getpath(element)
        if element.text == '$':
            xpaths.append('/' + path)
    return xpaths

# plurrr = etree.ElementTree(html.document_fromstring(fetch_html('https://plurrrr.com/')))

# for x in xpaths:
#     matches = plurrr.xpath(x)
#     for element in matches:
#         print(x, element.text)
