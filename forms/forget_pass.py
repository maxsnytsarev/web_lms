from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class forget_pass_1(FlaskForm):
    email = EmailField('Введите email*', validators=[DataRequired()])
    submit = SubmitField('Дальше')
