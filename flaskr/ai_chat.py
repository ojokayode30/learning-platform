import os
import random

from flask import (Blueprint, render_template, request, session, jsonify)
from flaskr.db import get_db
from flaskr.auth import login_required
import replicate

system_prompt = "You are a helpful, respectful and honest AI. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."

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
  introduction = replicate.run(
    "meta/llama-2-70b-chat",
    input={
        "prompt": "Tell me about " + course['title'] + " and give few suggestions on the topic \n return result using markdown",
        "top_k": 0,
        "top_p": 1,
        "max_tokens": 512,
        "temperature": 0.5,
        "system_prompt": system_prompt,
        "length_penalty": 1,
        "max_new_tokens": 500,
        "min_new_tokens": -1,
        "prompt_template": "<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
        "presence_penalty": 0,
        "log_performance_metrics": False
    },
  )
  introduction = ''.join(introduction)
  # course_suggestions = replicate.run(
  #   "meta/llama-2-70b-chat",
  #   input={
  #       "prompt": "Give few suggestions on " + course['title'] + "\n return result using markdown",
  #       "top_k": 0,
  #       "top_p": 1,
  #       "max_tokens": 512,
  #       "temperature": 0.5,
  #       "system_prompt": system_prompt,
  #       "length_penalty": 1,
  #       "max_new_tokens": 500,
  #       "min_new_tokens": -1,
  #       "prompt_template": "<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
  #       "presence_penalty": 0,
  #       "log_performance_metrics": False
  #   },
  # )
  # course_suggestions = ''.join(course_suggestions)
  return render_template('chat.html', course=course, intro=introduction)

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
    if course != "":
      system_prompt = "Return a response saying 'I can only answer questions related to " + course + "' when the question is not greetings or pleasantries and not related or similar to " + course + " and give just a simple brief."
    else:
      system_prompt = "You are a helpful, respectful and honest AI. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."

    response['ai'] = replicate.run(
      "meta/llama-2-70b-chat",
      input={
          "prompt": message,
          "system_prompt": system_prompt,
      },
    )

  return jsonify({ 'message': response })