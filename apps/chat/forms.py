from flask_wtf import FlaskForm
from wtforms import  TextAreaField
from wtforms.validators import DataRequired

# Chat


class ChatForm(FlaskForm):
    chat = TextAreaField('Prompt',
                         id='prompt',
                         validators=[DataRequired()])
