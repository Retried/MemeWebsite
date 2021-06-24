from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=256)])
    login = SubmitField('Zaloguj się')


class RegisterForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=256)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    register = SubmitField('Zarejestruj się')


class UploadForm(FlaskForm):
    title = StringField('Tytuł', validators=[InputRequired(), Length(min=1, max=24)])
    picture = FileField('Dodaj mema', validators=[FileAllowed(['jpg', 'png'])])
    send = SubmitField('Prześlij')


class AvatarForm(FlaskForm):
    picture = FileField('Zaktualizuj zdjecie', validators=[FileAllowed(['jpg', 'png'])])
    save = SubmitField('Zapisz')


class PointsForm(FlaskForm):
    point = SubmitField('+1')
