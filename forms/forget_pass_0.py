from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class forget_pass_0(FlaskForm):
    email = EmailField('Введите email*', validators=[DataRequired()])
    code = PasswordField('Введите кодовое слово', validators=[DataRequired()])
    submit = SubmitField('Дальше')
    id='1'