import os
from flask import (Flask, render_template, redirect, url_for)
from . import auth
from . import course
from . import ai_chat
from flaskr.auth import login_required

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
    return render_template('dashboard.html')

  @app.route('/hello')
  def hello():
    return 'Hello there!'
  
  from . import db
  db.init_app(app)

  app.register_blueprint(auth.bp)
  app.register_blueprint(course.bp)
  app.register_blueprint(ai_chat.bp)
  
  return app