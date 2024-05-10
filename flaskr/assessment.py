import os
from flask import Blueprint, render_template, session
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression

bp = Blueprint('assessment', __name__, url_prefix='/assessment')

@bp.route('/')
def assessment():
  # Get the user ID from the session
  user_id = session.get('user_id')
  
  # Connect to the SQLite database
  conn = sqlite3.connect(os.path.join('instance/flaskr.sqlite'))

  # Define SQL queries to retrieve relevant data
  user_enrollment_query = f"""
    SELECT c.title AS course_title, COUNT(ue.user_id) AS enrollment_count
    FROM courses c
    LEFT JOIN user_course_enrollment ue ON c.id = ue.course_id
    WHERE ue.user_id = '{user_id}'
    GROUP BY c.title
  """

  lesson_completion_query = f"""
    SELECT c.title AS course_title, l.title AS lesson_title,
    SUM(CASE WHEN ulp.completed = 1 THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN ulp.understood = 1 THEN 1 ELSE 0 END) AS understood_count,
    COUNT(*) AS total_lessons
    FROM courses c
    LEFT JOIN lessons l ON c.id = l.course_id
    LEFT JOIN user_lesson_progress ulp ON l.id = ulp.lesson_id
    WHERE ulp.user_id = '{user_id}'
    GROUP BY c.title, l.title
  """

  # Execute SQL queries and load results into Pandas DataFrames
  user_enrollment_df = pd.read_sql(user_enrollment_query, conn)
  lesson_completion_df = pd.read_sql(lesson_completion_query, conn)

  # Perform machine learning analysis
  # Let's perform linear regression on enrollment counts and completed counts
  x = lesson_completion_df[['understood_count']].values
  y = lesson_completion_df[['completed_count']].values

  model = LinearRegression()
  model.fit(x, y)
  predicted_completed_counts = model.predict(x)

  # Add the predicted completed counts to the lesson_completion_df DataFrame
  lesson_completion_df['predicted_completed_count'] = predicted_completed_counts

  # Bar chart data
  bar_chart_data = {
    'labels': lesson_completion_df['course_title'].tolist(),
    'enrollment_counts': user_enrollment_df['enrollment_count'].tolist(),
    'completed_counts': lesson_completion_df['completed_count'].tolist(),
    'understood_counts': lesson_completion_df['understood_count'].tolist(),
    'predicted_completed_counts': lesson_completion_df['predicted_completed_count'].tolist(),
    # Add more data as needed for other charts
  }

  # Close database connection
  conn.close()

  # Pass the data to the template
  return render_template('assessment.html', user_enrollment_df=user_enrollment_df, lesson_completion_df=lesson_completion_df, bar_chart_data=bar_chart_data)

@bp.route('/admin')
def admin_assessment():
  # Connect to the SQLite database
  conn = sqlite3.connect(os.path.join('instance/flaskr.sqlite'))

  # Define SQL queries to retrieve relevant data
  user_enrollment_query = """
    SELECT c.title AS course_title, COUNT(ue.user_id) AS enrollment_count
    FROM courses c
    LEFT JOIN user_course_enrollment ue ON c.id = ue.course_id
    GROUP BY c.title
  """

  lesson_completion_query = """
    SELECT c.title AS course_title, l.title AS lesson_title,
    SUM(CASE WHEN ulp.completed = 1 THEN 1 ELSE 0 END) AS completed_count,
    COUNT(*) AS total_lessons
    FROM courses c
    LEFT JOIN lessons l ON c.id = l.course_id
    LEFT JOIN user_lesson_progress ulp ON l.id = ulp.lesson_id
    GROUP BY c.title, l.title
  """

  ai_evaluations_query = """
    SELECT name AS model_name, evaluation_metric, AVG(value) AS average_value
    FROM ai_models
    JOIN evaluations ON ai_models.id = evaluations.ai_model_id
    GROUP BY model_name, evaluation_metric
  """

  # Execute SQL queries and load results into Pandas DataFrames
  user_enrollment_df = pd.read_sql(user_enrollment_query, conn)
  lesson_completion_df = pd.read_sql(lesson_completion_query, conn)
  ai_evaluations_df = pd.read_sql(ai_evaluations_query, conn)

  # Perform data analysis...

  # Close database connection
  conn.close()

  # Pass the data to the template
  return render_template('admin/assessment.html', user_enrollment_df=user_enrollment_df, lesson_completion_df=lesson_completion_df, ai_evaluations_df=ai_evaluations_df)
