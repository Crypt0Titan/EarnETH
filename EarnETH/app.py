import sys
import os
from datetime import datetime
from flask import Flask, render_template
from jinja2 import ChoiceLoader, FileSystemLoader
from extensions import db, socketio, csrf
import eventlet
from admin_auth import admin_auth as admin_auth_blueprint

eventlet.monkey_patch()

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def create_app():
    app = Flask(__name__, static_folder=os.path.join(project_root, 'static'))

    # Set up multiple template folders
    template_folders = [
        os.path.join(project_root, 'templates'),
        project_root  # This allows Flask to look in the root directory and its subdirectories
    ]
    app.jinja_loader = ChoiceLoader([FileSystemLoader(folder) for folder in template_folders])

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or '7ab1b1c0m32dub41y4114y45ar4'  # Replace in production

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)  # This initializes the Socket.IO instance with Flask
    csrf.init_app(app)  # Apply CSRF protection globally

    # Register blueprints
    app.register_blueprint(admin_auth_blueprint)

    from main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from Games.Wordle.wordle_routes import wordle
    app.register_blueprint(wordle, url_prefix='/wordle')

    from Games.FlappyBirds.flappybirds_routes import flappybirds
    app.register_blueprint(flappybirds, url_prefix='/flappybirds')

    from Games.Snake.snake_routes import snake
    app.register_blueprint(snake, url_prefix='/snake')

    from Games.TicTacToe.tictactoe_routes import tic_tac_toe
    app.register_blueprint(tic_tac_toe, url_prefix='/tictactoe')

    @app.context_processor
    def inject_now():
        # Use UTC for all times in templates
        return {'now': datetime.utcnow()}

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
