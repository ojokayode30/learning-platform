import os
from flask import (Flask, render_template)

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
  
  @app.route('/dashboard')
  def dashboard():
    return render_template('dashboard.html')

  @app.route('/hello')
  def hello():
    return 'Hello there!'
  
  from . import db
  db.init_app(app)

  from . import auth
  app.register_blueprint(auth.bp)
  
  return app