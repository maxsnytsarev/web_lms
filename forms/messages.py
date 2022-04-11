from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class Message(FlaskForm):
    mess = StringField('a')
    submit = SubmitField('Написать')
    submit_new = SubmitField('update')
