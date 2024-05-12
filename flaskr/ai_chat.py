import os
import random

from flask import (Blueprint, render_template, request, session, jsonify)
from flaskr.db import get_db
from flaskr.auth import login_required
from openai import OpenAI
import google.generativeai as genai
import requests
import replicate

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
@login_required
def index():
  return render_template('chat.html')

@bp.route('/<course_id>/course')
@login_required
def chat(course_id):
  db = get_db()
  # ai = MetaAI(proxy=proxy)
  course = db.execute(
    "SELECT * FROM courses WHERE id = ?", (course_id,)
  ).fetchone()
  intro = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "prompt": "Tell me about " + course['title'],
        "system_prompt": '',
    },
  )
  course_suggestions = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "prompt": "Give few suggestions on " + course['title'],
        "system_prompt": '',
    },
  )
  return render_template('chat.html', course=course, intro=intro, course_suggestions=course_suggestions)

@bp.route('/message', methods=('POST',))
@login_required
def message():
  user_id = session.get('user_id')
  message = request.json['message']
  chattype = request.json['type']
  course = request.json['course']
  response = {}

  if chattype == 'instructor':
    # Add random message response related to course instructor
    responses = [
      "Sure, I'm here to assist you every step of the way.",
      "That's an interesting question. Let me provide some insight.",
      "I appreciate your curiosity! Let's dive into the topic together.",
      "Absolutely, I'm happy to guide you through any questions you have.",
      "Let's explore this topic further. Feel free to ask anything.",
      "Your curiosity is commendable! Let's find the answer together.",
      "I'm glad you asked! Let me provide some clarity on that.",
      "Excellent question! Let me shed some light on the topic.",
      "Your engagement is appreciated! Let's delve into the details.",
      "Of course! I'm here to provide support and clarification.",
      "Thanks for reaching out! Let's tackle this question together.",
      "Your interest in learning is admirable! Let's find the answer.",
      "Absolutely, I'm here to address any inquiries you may have.",
      "I'm excited to help you explore this topic further.",
      "Your dedication to learning is evident! Let's dive in."
    ]
    response['instructor'] = random.choice(responses)
  else:
    if course is not None:
      system_prompt = "Return a response saying 'I can only answer questions related to " + course + "' when the question is not pleasantries and not related or similar to " + course + " and give just a simple brief."

      response['ai'] = replicate.run(
        "meta/llama-2-70b-chat",
        input={
            "prompt": message,
            "system_prompt": system_prompt,
        },
      )

  return jsonify({ 'message': response })