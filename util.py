import base64
import os
import uuid
import urllib.request

from lucid.db import get_db

from flask import current_app

from pygments            import highlight
from pygments.lexers     import HtmlLexer
from pygments.formatters import HtmlFormatter



def new_feed_name():
    # Generate a new, unique feed name using a random UUID.
    # Uniqueness is important because feed names are used to identify
    # files associated with each feed; name collisions would
    # compromise the integrity of the service.
    u = uuid.uuid4()
    # base64 encode UUID to make it a little less unwieldy, and remove
    # padding (we won't ever need to decode it)
    return base64.urlsafe_b64encode(u.bytes).decode('utf-8')[:-2]


def feed_html_path(feed):
    filename = feed + '.html'
    return os.path.join(current_app.config['TMP'], filename)

def feed_rss_path(feed):
    filename = feed + '.xml'
    return os.path.join(current_app.config['RSS'], filename)


def feed_exists(feed):
    db = get_db()
    feeds = db.execute("SELECT * FROM feed WHERE name=?", (feed,)).fetchall()
    return (len(feeds) != 0)



def save_page(feed, url):
    path = feed_html_path(feed)
    try:
        urllib.request.urlretrieve(url, path)
    except:
        return False
    else:
        return True
    
def pygmentize_html(feed):
    path = feed_html_path(feed)
    f = open(path, 'r', encoding='utf-8')
    html = f.read()
    f.close()
    return highlight(html, HtmlLexer(), HtmlFormatter())
