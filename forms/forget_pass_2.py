from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class forget_pass_2(FlaskForm):
    newpass1 = StringField('Введите новый пароль*', validators=[DataRequired()])
    newpass2 = StringField('Повторите пароль*', validators=[DataRequired()])
    submit = SubmitField('Изменить')
    id=''