import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import lucid.util as util
from   lucid.db import get_db


bp = Blueprint('index', __name__, url_prefix='/')



def make_feed(url):
    db = get_db()
    error = None

    if not url:
        error = "Missing URL."
        
    if error is None:
        try:
            name = util.new_feed_name()
            db.execute("INSERT INTO feed (name, url) VALUES (?, ?)",
                       (name, url))
            db.commit()
        except db.IntegrityError:
            error = f"The feed {name} already exists."

    if error is not None:
        flash(error)
    

def delete_feed(feed):
    db = get_db()
    db.execute("DELETE FROM feed WHERE name=?", (feed,))
    db.commit()



@bp.route('/', methods=('GET', 'POST'))
def show_index():
    db = get_db()
    feeds = db.execute('SELECT name, url FROM feed').fetchall()
    
    if request.method == 'POST':
        if 'URL' in request.form:
            make_feed(request.form['URL'])
        if 'delete' in request.form:
            delete_feed(request.form['delete'])
        return redirect(url_for('index.show_index'))
    else:
        return render_template('/index.html', feeds=feeds)
