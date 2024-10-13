from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_wtf.csrf import CSRFProtect
from models import FlappyPlayer
from extensions import db, csrf
from forms import ResetFlappyBirdScoresForm

flappybirds = Blueprint('flappybirds', __name__)

@flappybirds.route('/flappybirds')
def flappybirds_home():
    return render_template('Games/FlappyBirds/flappy_birds.html')

@flappybirds.route('/submit_flappy_score', methods=['POST'])
@csrf.exempt
def submit_flappy_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        wallet_address = data.get('wallet_address')
        score = data.get('score')

        if not wallet_address or score is None:
            return jsonify({"success": False, "message": "Missing wallet address or score"}), 400

        flappy_player = FlappyPlayer.query.filter_by(ethereum_address=wallet_address).first()
        if flappy_player:
            if score > flappy_player.high_score:
                flappy_player.high_score = score
                db.session.commit()
        else:
            new_player = FlappyPlayer(ethereum_address=wallet_address, high_score=score)
            db.session.add(new_player)
            db.session.commit()

        return jsonify({"success": True, "message": "Score submitted successfully."})
    except Exception as e:
        current_app.logger.error(f"Error submitting score: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@flappybirds.route('/flappy_birds_stats')
def flappy_birds_stats():
    form = ResetFlappyBirdScoresForm()  # Create a form instance
    players = FlappyPlayer.query.order_by(FlappyPlayer.high_score.desc()).all()
    return render_template('Games/FlappyBirds/flappy_birds_stats.html', players=players, form=form)

@flappybirds.route('/reset_flappy_scores', methods=['POST'])
def reset_flappy_scores():
    form = ResetFlappyBirdScoresForm()  # Ensure CSRF validation
    if form.validate_on_submit():
        try:
            FlappyPlayer.query.update({FlappyPlayer.high_score: 0})
            db.session.commit()
            flash('All Flappy ETH game scores have been reset to zero.', 'success')
        except Exception as e:
            current_app.logger.error(f"Error resetting scores: {str(e)}")
            db.session.rollback()
            flash(f'Error resetting scores: {str(e)}', 'error')
    return redirect(url_for('flappybirds.flappy_birds_stats'))

@flappybirds.route('/get_flappy_rank/<ethereum_address>', methods=['GET'])
def get_flappy_rank(ethereum_address):
    try:
        players = FlappyPlayer.query.order_by(FlappyPlayer.high_score.desc()).all()
        for index, player in enumerate(players, start=1):
            if player.ethereum_address == ethereum_address:
                return jsonify({'success': True, 'rank': index})
        return jsonify({'success': False, 'message': 'Player not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting player rank: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500