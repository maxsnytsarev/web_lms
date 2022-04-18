from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта*', validators=[DataRequired()])
    password = PasswordField('Пароль*', validators=[DataRequired()])
    password_again = PasswordField('Пароль (подтвердить)*', validators=[DataRequired()])
    first_name = StringField('Имя*', validators=[DataRequired()])
    second_name = StringField('Фамилия*', validators=[DataRequired()])
    # second_nam = StringField('Фамилия*')
    code = StringField("Кодовое слово*", validators=[DataRequired()])
    about = TextAreaField("О вас")
    submit = SubmitField('Зарегистрироваться')
