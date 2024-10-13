from models import SnakePlayer, WordlePlayer, FlappyPlayer  # Updated imports
from sqlalchemy import func
from extensions import db, socketio
import pytz
from datetime import datetime, timedelta, timezone

def check_answers(questions, submitted_answers):
    score = 0
    for question, answer in zip(questions, submitted_answers):
        if question.answer.lower() == answer.lower():
            score += 1
    return score

# Removed determine_winner function related to WTW

# Removed calculate_game_statistics function related to WTW

def make_aware(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt

# utils.py
import datetime
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import logging

socketio = SocketIO()
db = SQLAlchemy()
logger = logging.getLogger(__name__)

# Removed update_game_statuses function related to WTW
