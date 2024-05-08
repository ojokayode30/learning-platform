import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('course', __name__, url_prefix='/course')

@bp.route('/')
@login_required
def index():
  user_id = session.get('user_id')
  db = get_db()
  courses = db.execute("SELECT * FROM courses").fetchall()
  enrolled_courses = db.execute("""
    SELECT courses.id, courses.title, courses.description, courses.instructor
    FROM user_course_enrollment
    JOIN courses ON user_course_enrollment.course_id = courses.id
    WHERE user_course_enrollment.user_id = ?
  """, (user_id,)).fetchall()
  
  return render_template('course/index.html', courses=courses, enrolled_courses=enrolled_courses)

@bp.route('/enroll/<course_id>')
@login_required
def enroll(course_id):
  user_id = session.get('user_id')
  db = get_db()
  enrollment_exists = db.execute("SELECT 1 FROM user_course_enrollment WHERE user_id = ? AND course_id = ?", (user_id, course_id)).fetchone()
  if enrollment_exists:
        flash("You are already enrolled in this course.")
  else:
    db.execute("INSERT INTO user_course_enrollment (user_id, course_id) VALUES (?, ?)", (user_id, course_id))
    db.commit()
    flash("Successfully enrolled in the course.")
  return redirect(url_for('course.index'))

@bp.route('/unenroll/<course_id>')
@login_required
def uneroll(course_id):
  user_id = session.get('user_id')
  db = get_db()
  enrollment_exists = db.execute(
    "SELECT 1 FROM user_course_enrollment WHERE user_id = ? AND course_id = ?",
    (user_id, course_id)
  ).fetchone()

  if enrollment_exists:
    db.execute(
      "DELETE FROM user_course_enrollment WHERE user_id = ? AND course_id = ?",
      (user_id, course_id))
    db.commit()
    flash("Successfully unenrolled from the course.")
  else:
    flash("You are not currently enrolled in this course.")

  return redirect(url_for('course.index'))

@bp.route('/<course_id>/lessons')
@login_required
def course_lessons(course_id):
  user_id = session.get('user_id')
  db = get_db()
  course = db.execute(
    "SELECT * FROM courses WHERE id = ?", (course_id,)
  ).fetchone()

  lessons = db.execute("""
    SELECT l.*, ulp.completed, ulp.understood
    FROM lessons l
    LEFT JOIN user_lesson_progress ulp ON l.id = ulp.lesson_id AND ulp.user_id = ?
    WHERE l.course_id = ?
  """, (user_id, course_id)).fetchall()

  enrolled = db.execute(
    "SELECT COUNT(*) FROM user_course_enrollment WHERE user_id = ? AND course_id = ?",
    (user_id, course_id)
  ).fetchone()[0] > 0
  
  return render_template('course/lessons.html', course=course, lessons=lessons, enrolled=enrolled)

@bp.route('/lessons_progress/<lesson_id>/<is_complete>')
@login_required
def course_lessons_progress(lesson_id, is_complete):
  user_id = session.get('user_id')
  db = get_db()
  
  # Convert the is_complete parameter to a boolean value
  if is_complete.lower() == 'done':
    completed = True
  else:
    completed = False
  
  # Check if the lesson exists
  lesson = db.execute(
    "SELECT * FROM lessons WHERE id = ?", (lesson_id,)
  ).fetchone()
  
  if lesson is None:
    flash('Lesson not found', 'error')
    return redirect(request.referrer)

  # Check if the user has already recorded progress for this lesson
  existing_progress = db.execute(
    "SELECT * FROM user_lesson_progress WHERE user_id = ? AND lesson_id = ?",
    (user_id, lesson_id)
  ).fetchone()

  if existing_progress:
    # Update existing progress
    db.execute(
      "UPDATE user_lesson_progress SET completed = ? WHERE user_id = ? AND lesson_id = ?",
      (completed, user_id, lesson_id)
    )
  else:
    # Insert new progress
    db.execute(
      "INSERT INTO user_lesson_progress (user_id, lesson_id, completed) VALUES (?, ?, ?)",
      (user_id, lesson_id, completed)
    )

  db.commit()
  
  return redirect(request.referrer)

@bp.route('/lessons_understanding/<lesson_id>/<is_understood>')
@login_required
def course_lessons_unserstanding(lesson_id, is_understood):
  user_id = session.get('user_id')
  db = get_db()
  
  # Convert the is_complete parameter to a boolean value
  if is_understood.lower() == 'yes':
    understood = True
  else:
    understood = False
  
  # Check if the lesson exists
  lesson = db.execute(
    "SELECT * FROM lessons WHERE id = ?", (lesson_id,)
  ).fetchone()
  
  if lesson is None:
    flash('Lesson not found', 'error')
    return redirect(request.referrer)

  # Check if the user has already recorded progress for this lesson
  existing_progress = db.execute(
    "SELECT * FROM user_lesson_progress WHERE user_id = ? AND lesson_id = ?",
    (user_id, lesson_id)
  ).fetchone()

  if existing_progress:
    # Update existing progress
    db.execute(
      "UPDATE user_lesson_progress SET understood = ? WHERE user_id = ? AND lesson_id = ?",
      (understood, user_id, lesson_id)
    )
  else:
    # Insert new progress
    db.execute(
      "INSERT INTO user_lesson_progress (user_id, lesson_id, completed, understood) VALUES (?, ?, ?, ?)",
      (user_id, lesson_id, 0, understood)
    )

  db.commit()
  
  return redirect(request.referrer)