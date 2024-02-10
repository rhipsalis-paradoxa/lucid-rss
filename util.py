import base64
import uuid
import urllib.request

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


def fetch_html(url):
    try:
        response = urllib.request.urlopen(url)
    except URLError:
        return "Error opening URL."
    else:
        return response.read().decode('utf-8')



# TODO: output HTML to file
def pygmentize_from_url(url):
    html = fetch_html(url)
    highlighted = highlight(html, HtmlLexer(), HtmlFormatter())
    return highlighted
