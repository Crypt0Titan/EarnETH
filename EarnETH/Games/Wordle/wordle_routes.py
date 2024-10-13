from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models import WordlePlayer, DailyWord
from extensions import db, csrf
from datetime import date
from forms import ResetWordleScoresForm
import random


wordle = Blueprint('wordle', __name__)

@wordle.route('/wordle')
def wordle_home():
    return render_template('Games/Wordle/wordle.html')

@wordle.route('/get_daily_words', methods=['GET'])
def get_daily_words():
    wallet_address = request.args.get('wallet_address')
    if not wallet_address:
        return jsonify({"success": False, "message": "Wallet address is required"}), 400

    player = WordlePlayer.query.filter_by(ethereum_address=wallet_address).first()
    if not player:
        player = WordlePlayer(ethereum_address=wallet_address, games_played=0, total_score=0)
        db.session.add(player)
        db.session.commit()

    daily_words = DailyWord.query.filter_by(date=date.today()).all()
    words = [word.word for word in daily_words]

    # Shuffle the daily words
    random.shuffle(words)

    remaining_games = 10 - player.games_played

    return jsonify({
        "success": True,
        "words": words,
        "remaining_games": remaining_games
    })

@wordle.route('/submit_wordle_score', methods=['POST'])
@csrf.exempt
def submit_wordle_score():
    data = request.json
    wallet_address = data.get('wallet_address')
    score = data.get('score')

    if not wallet_address or score is None:
        return jsonify({"success": False, "message": "Missing wallet address or score"}), 400

    player = WordlePlayer.query.filter_by(ethereum_address=wallet_address).first()

    if player:
        # Check if the day has changed, reset daily games if necessary
        if player.last_reset_date != date.today():
            player.daily_games_played = 0
            player.last_reset_date = date.today()

        # Increment games played and total score
        player.total_score += score
        player.daily_games_played += 1
        player.games_played += 1

        # Check if the player has completed a session (10 games in total)
        if player.games_played >= 10:
            player.sessions_played += 1
            player.games_played = 0  # Reset games played for a new session

        db.session.commit()
    else:
        # Create a new player entry if they don't exist
        player = WordlePlayer(
            ethereum_address=wallet_address, 
            total_score=score, 
            games_played=1,
            daily_games_played=1,
            last_reset_date=date.today()
        )
        db.session.add(player)
        db.session.commit()

    rank = WordlePlayer.query.filter(WordlePlayer.total_score > player.total_score).count() + 1
    remaining_games = 10 - player.daily_games_played  # Update remaining games for today

    return jsonify({
        'success': True,
        'message': 'Score submitted successfully',
        'rank': rank,
        'remaining_games': remaining_games
    })



@wordle.route('/wordle_stats')
def wordle_stats():
    form = ResetWordleScoresForm()  # Create a form instance
    players = WordlePlayer.query.order_by(WordlePlayer.total_score.desc()).all()
    daily_words = DailyWord.query.filter_by(date=date.today()).all()
    return render_template('Games/Wordle/wordle_stats.html', players=players, daily_words=daily_words, form=form)

@wordle.route('/add_daily_words', methods=['POST'])
def add_daily_words():
    today = date.today()
    DailyWord.query.filter_by(date=today).delete()
    for i in range(10):
        word = request.form.get(f'word{i}')
        if word and len(word) == 5:
            new_word = DailyWord(word=word.lower(), date=today)
            db.session.add(new_word)
    db.session.commit()
    flash('Daily words have been updated', 'success')
    return redirect(url_for('wordle.wordle_stats'))

@wordle.route('/reset_wordle_scores', methods=['POST'])
def reset_wordle_scores():
    try:
        # Completely clear all records from the WordlePlayer table
        WordlePlayer.query.delete()
        db.session.commit()
        flash('All Wordle player data has been removed.', 'success')
    except Exception as e:
        current_app.logger.error(f"Error resetting Wordle player data: {str(e)}")
        db.session.rollback()
        flash(f'Error resetting player data: {str(e)}', 'error')
    return redirect(url_for('wordle.wordle_stats'))


@wordle.route('/reset_daily_words', methods=['POST'])
def reset_daily_words():
    form = ResetWordleScoresForm()  # Ensure CSRF validation
    if form.validate_on_submit():
        DailyWord.query.filter_by(date=date.today()).delete()
        db.session.commit()
        flash('Daily words have been reset', 'success')
    return redirect(url_for('wordle.wordle_stats'))