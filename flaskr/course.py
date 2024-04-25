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
  lessons = db.execute(
    "SELECT * FROM lessons WHERE course_id = ?", (course_id,)
  ).fetchall()
  return render_template('course/lessons.html', course=course, lessons=lessons)