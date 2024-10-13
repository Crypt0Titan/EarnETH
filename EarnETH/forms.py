from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ResetSnakeScoresForm(FlaskForm):
    pass  # Since no fields are needed, this is just an empty form to handle CSRF protection

class ResetFlappyBirdScoresForm(FlaskForm):
    pass  # No fields, just CSRF protection

class ResetWordleScoresForm(FlaskForm):
    pass  # No fields, just CSRF protection