import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import lucid.util as util
from   lucid.db import get_db


bp = Blueprint('create', __name__, url_prefix='/create')


@bp.route('/', methods=('GET', 'POST'))
def create():
    return render_template('/create.html')
