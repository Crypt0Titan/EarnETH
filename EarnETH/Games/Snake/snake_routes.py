from flask import Blueprint, render_template, request, jsonify, current_app
from flask_wtf.csrf import CSRFProtect
from models import SnakePlayer
from extensions import db, csrf
import json
from forms import ResetSnakeScoresForm

snake = Blueprint('snake', __name__)

@snake.route('/snake')
def snake_home():
    return render_template('Games/Snake/snake_game.html')

@snake.route('/submit_snake_score', methods=['POST'])
@csrf.exempt
def submit_snake_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        wallet_address = data.get('wallet_address')
        score = data.get('score')

        if not wallet_address or score is None:
            return jsonify({"success": False, "message": "Missing wallet address or score"}), 400

        snake_player = SnakePlayer.query.filter_by(ethereum_address=wallet_address).first()
        if snake_player:
            if score > snake_player.high_score:
                snake_player.high_score = score
                db.session.commit()
        else:
            new_player = SnakePlayer(ethereum_address=wallet_address, high_score=score)
            db.session.add(new_player)
            db.session.commit()

        return jsonify({"success": True, "message": "Score submitted successfully."})
    except Exception as e:
        current_app.logger.error(f"Error submitting score: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@snake.route('/get_player_rank/<ethereum_address>', methods=['GET'])
def get_player_rank(ethereum_address):
    try:
        players = SnakePlayer.query.order_by(SnakePlayer.high_score.desc()).all()
        for index, player in enumerate(players, start=1):
            if player.ethereum_address == ethereum_address:
                return jsonify({'success': True, 'rank': index})
        return jsonify({'success': False, 'message': 'Player not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting player rank: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@snake.route('/snake_stats')
def snake_stats():
    form = ResetSnakeScoresForm()  # Create an instance of the form
    players = SnakePlayer.query.order_by(SnakePlayer.high_score.desc()).all()
    return render_template('Games/Snake/snake_stats.html', form=form, players=players)

@snake.route('/reset_snake_scores', methods=['POST'])
def reset_snake_scores():
    form = ResetSnakeScoresForm()  # Validate the form
    if form.validate_on_submit():  # Ensure CSRF validation passes
        try:
            SnakePlayer.query.update({SnakePlayer.high_score: 0})
            db.session.commit()
            return jsonify({"success": True, "message": "All snake game scores have been reset to zero."})
        except Exception as e:
            current_app.logger.error(f"Error resetting scores: {str(e)}")
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
    return jsonify({"success": False, "message": "Invalid form submission."}), 400