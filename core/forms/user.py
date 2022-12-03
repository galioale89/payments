import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class UserForm(FlaskForm):
    name = StringField("Nome", [validators.DataRequired(), validators.length(min=1, max=100)])
    nickname = StringField("Usuário", [validators.DataRequired(), validators.length(min=1, max=10)])
    password = PasswordField("Senha", [validators.DataRequired(), validators.length(min=1, max=100)])
    login = SubmitField("Login")