from crypt import methods
import email
from nturl2path import url2pathname
from flask_login import login_required, login_user, logout_user
from . import auth
from flask import render_template, redirect, url_for, request, flash
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, firstname=form.firstname.data,
                    lastname=form.lastname.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',registration_form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('views.index'))
        
        flash('uh oh, seems like your details were wrong')
        
    return render_template('auth/login.html', login_form=login_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))
