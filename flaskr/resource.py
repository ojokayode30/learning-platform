import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flaskr.auth import login_required
from meta_ai_api import MetaAI

bp = Blueprint('resource', __name__, url_prefix='/resource')

@bp.route('/')
@login_required
def index():
  user_id = session.get('user_id')
  db = get_db()
  return render_template('resource.html')