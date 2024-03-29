import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import lucid.util as util
import lucid.parser as parser
from   lucid.db import get_db
import lucid.llm as llm



bp = Blueprint('create', __name__, url_prefix='/')


@bp.route('/create/<feed>', methods=('GET', 'POST'))
def create(feed):
    if not util.feed_exists(feed):
        return f"The feed with ID {feed} was not found.", 404
    
    pyg = util.pygmentize_html(feed)
    return render_template('/create.html', html=pyg)


@bp.route('/create/<feed>/preview', methods=('POST',))
def preview(feed):
    if not util.feed_exists(feed):
        return f"The feed with ID {feed} was not found.", 404

    in_template  = request.form['input-template']
    out_template = request.form['output-template']
    xpaths   = parser.xpaths_from_template(in_template)
    if xpaths is None:
        return f"Error: webpage is not valid HTML."

    articles = parser.extract_articles(feed, xpaths)
    if articles is None:
        return f"Error: input template is not valid HTML."
    
    s = ''
    print(articles)
    for a in articles:
        f = parser.fmt_article(out_template, a)
        s += "\n" + f
    return s


@bp.route('/create/<feed>/hint', methods=('POST',))
def suggest(feed):
    if not util.feed_exists(feed):
        return f"The feed with ID {feed} was not found.", 404

    in_template  = request.form['input-template']
    out_template = request.form['output-template']

    in_hint  = llm.html_hint(in_template)
    out_hint = llm.html_hint(out_template)

    print(in_hint)
    print(out_hint)
    
    return {'in_hint': in_hint, 'out_hint': out_hint}
     
