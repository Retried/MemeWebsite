from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=256)])
    remember = BooleanField('Zapamiętaj mnie')


class RegisterForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=256)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
