from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from core.models.user import User
from core.forms.user import UserForm
from flask_bcrypt import check_password_hash

logon = Blueprint("logon", __name__, template_folder="template")
api = '/login'

@logon.route(f'{api}/')
def login():
    next = request.args.get('next')
    form = UserForm()
    return render_template('login.html', form=form, next=next)

@logon.route(f'{api}/autenticar', methods=['POST',])
def autenticar():
    form = UserForm(request.form)
    user = User.query.filter_by(nickname=form.nickname.data).first()
    password = check_password_hash(user.password, form.password.data)

    if user and password:
        session['loguser'] = user.nickname
        flash(f'{user.nickname} logado')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('logon.login'))

@logon.route(f'{api}/logout')
def logout():
    session["loguser"] = None
    flash("Lgout efetuado com sucesso")
    return redirect(url_for("logon.login"))