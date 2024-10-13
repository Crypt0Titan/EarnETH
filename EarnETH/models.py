from extensions import db
from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float

def get_current_utc_time():
    """Returns the current UTC time as a timezone-aware datetime object."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)

# Snake Player Stats
class SnakePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ethereum_address = db.Column(db.String(255), unique=True, nullable=False)
    high_score = db.Column(db.Integer, nullable=False, default=0)

# Wordle
class WordlePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ethereum_address = db.Column(db.String(42), unique=True, nullable=False)
    total_score = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    daily_games_played = db.Column(db.Integer, default=0)  # Track daily games played
    last_reset_date = db.Column(db.Date, default=date.today)  # Track the last reset date
    sessions_played = db.Column(db.Integer, default=0)  # Track total sessions played


    def __repr__(self):
        return f'<WordlePlayer {self.ethereum_address}, Score: {self.score}, Total: {self.total_score}, Games: {self.games_played}>'

# Define TicTacToePlayer model
class TicTacToePlayer(db.Model):
    __tablename__ = 'tictactoe_players'  # Name the table
    id = db.Column(db.Integer, primary_key=True)
    ethereum_address = db.Column(db.String(42), unique=True, nullable=False)
    high_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<TicTacToePlayer {self.ethereum_address}, Score: {self.high_score}>'

class DailyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f'<DailyWord {self.word} for {self.date}>'

# Flappy ETH Class
class FlappyPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ethereum_address = db.Column(db.String(42), unique=True, nullable=False)
    high_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<FlappyPlayer {self.ethereum_address}>'

# Admin Model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Admin {self.username}>'
