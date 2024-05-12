import os
from flask import (Blueprint, render_template, session, current_app, request, jsonify)
from flaskr.auth import login_required
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import replicate

bp = Blueprint('assessment', __name__, url_prefix='/assessment')

@bp.route('/')
def assessment():
  # Get the user ID from the session
  user_id = session.get('user_id')
  
  # Connect to the SQLite database
  conn = sqlite3.connect(current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES)

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

@bp.route('/analysis', methods=('POST',))
@login_required
def analysis():
  understood = request.json['understood']
  completed = request.json['completed']
  course = request.json['course']
  lesson = request.json['lesson']

  if understood != "1":
    understood = "The student did not understand the lesson"
  else:
    understood = "The student did understand the lesson"

  if completed != "1":
    completed = "The student was not able to complete the lesson"
  else:
    completed = "The student was able to complete the lesson"

  prompt = """
    Make a comprehensive analysis for a student that took a course titled "{}" and the course lesson is titled "{}"

    Here are the following the student has done

    1. {}
    2. {}

    return result using markdown
  """.format(course, lesson, completed, understood)

  response = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "top_k": 0,
        "top_p": 1,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.5,
        "system_prompt": "You are a helpful, respectful and honest AI. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        "length_penalty": 1,
        "max_new_tokens": 500,
        "min_new_tokens": -1,
        "prompt_template": "<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
        "presence_penalty": 0,
        "log_performance_metrics": False
    },
  )

  return jsonify({ 'message': response })