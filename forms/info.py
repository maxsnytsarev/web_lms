from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class InfoForm(FlaskForm):
    # password = PasswordField('Пароль', validators=[DataRequired()])
    about = TextAreaField("О вас")
    submit = SubmitField('Зарегистрироваться')
