import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flaskr.auth import login_required
from meta_ai_api import MetaAI

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
@login_required
def index():
  user_id = session.get('user_id')
  db = get_db()
  return render_template('chat.html')

@bp.route('/<course_id>/course')
@login_required
def chat(course_id):
  user_id = session.get('user_id')
  db = get_db()
  ai = MetaAI()
  course = db.execute(
    "SELECT * FROM courses WHERE id = ?", (course_id,)
  ).fetchone()
  message = "Tell me about " + course['title']
  intro = ai.prompt(message=message)
  course_suggestions = ai.prompt(message="Give few suggestions on " + course['title'])
  return render_template('chat.html', course=course, intro=intro['message'], course_suggestions=course_suggestions['message'])

@bp.route('/ai-message', methods=('POST',))
@login_required
def message():
  message = request.json['message']
  print(message)
  user_id = session.get('user_id')
  db = get_db()
  ai = MetaAI()
  response = ai.prompt(message=message)
  return jsonify({ 'message': response })