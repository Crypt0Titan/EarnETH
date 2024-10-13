from flask import Blueprint, render_template

tic_tac_toe = Blueprint('tic_tac_toe', __name__)

@tic_tac_toe.route('/tictactoe')
def tictactoe_home():
    return render_template('Games/TicTacToe/tic_tac_toe.html')