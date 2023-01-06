from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import Email, DataRequired

# Chat


class ChatForm(FlaskForm):
    chat = TextAreaField('Prompt',
                         id='prompt',
                         validators=[DataRequired()])
