import os
from flask import (Flask, render_template, redirect, url_for, session, g)
from . import db
from . import auth
from . import course
from . import ai_chat
from . import resource
from . import assessment
from flaskr.auth import login_required
from flaskr.db import get_db

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY = 'LEARNING-PLATFORM',
    DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
  )

  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  @app.route('/')
  def index():
    return redirect(url_for('dashboard'))

  @app.route('/dashboard')
  @login_required
  def dashboard():
    user_id = session.get('user_id')
    db = get_db()

    # Total courses
    total_courses = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]

    # Total enrolled courses
    total_enrolled_courses = db.execute(
        "SELECT COUNT(*) FROM user_course_enrollment WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    # Completed courses
    completed_courses = db.execute("""
        SELECT COUNT(DISTINCT uce.course_id)
        FROM user_course_enrollment AS uce
        JOIN user_lesson_progress AS ulp ON uce.course_id = ulp.lesson_id
        WHERE uce.user_id = ? AND ulp.completed = 1
    """, (user_id,)).fetchone()[0]

    return render_template('dashboard.html', total_courses=total_courses, total_enrolled_courses=total_enrolled_courses, completed_courses=completed_courses)

  @app.route('/hello')
  def hello():
    return 'Hello there!'

  db.init_app(app)

  app.register_blueprint(auth.bp)
  app.register_blueprint(course.bp)
  app.register_blueprint(ai_chat.bp)
  app.register_blueprint(resource.bp)
  app.register_blueprint(assessment.bp)
  
  return app