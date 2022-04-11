from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    email_info = TextAreaField('Email')
    first_name = TextAreaField('Имя')
    second_name = TextAreaField('Фамилия')
