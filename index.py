import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import lucid.util as util
from   lucid.db import get_db

import validators



bp = Blueprint('index', __name__, url_prefix='/')



def make_feed(url):
    db = get_db()
    error = None
    name = util.new_feed_name()

    if not url or not validators.url(url):
        error = f"Missing or invalid URL: {url}."
    elif not util.save_page(name, url):
        error = f"Error saving page at URL: {url}."
        
    if error is None:
        try:
            db.execute("INSERT INTO feed (name, url) VALUES (?, ?)",
                       (name, url))
            db.commit()
        except db.IntegrityError:
            error = f"The feed {name} already exists."

    if error is not None:
        flash(error)
        return None

    return name
    

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
            url  = request.form['URL']
            name = make_feed(url)
            if name is not None:
                return redirect(url_for('create.create', feed=name))
            else:
                return redirect(url_for('index.show_index'))
        if 'delete' in request.form:
            delete_feed(request.form['delete'])
            return redirect(url_for('index.show_index'))

    return render_template('/index.html', feeds=feeds)
