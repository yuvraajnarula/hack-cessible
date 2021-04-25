from flask import Flask, redirect, request
from flask.helpers import flash, url_for
from flask_login import login_user, current_user, login_required
from flask.templating import render_template
from covid19 import app, login_manager, db
from covid19.forms import RegistrationForm, LoginForm, CreatePostForm
from covid19.models import User, Posts
import bcrypt


@app.route("/home")
@app.route("/")
def home():
    posts = Posts.query.all()
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        #print('login valid')
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('UTF-8'), user.password):
            login_user(user, remember=form.remember.data)
            flash('Successfully logged in', 'success')
            return redirect(url_for('home'))
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        #print('form valid')
        hashed_pw = bcrypt.hashpw(
            request.form['password'].encode('UTF-8'), bcrypt.gensalt())
        email = request.form['email']
        password = hashed_pw
        phone = request.form['phone']
        record = User(email, password, phone)
        db.session.add(record)
        db.session.commit()
    return render_template('register.html', title="Register", form=form)


@app.route("/post/create", methods=['GET', 'POST'])
# TODO: Uncomment this later on
@login_required
def createpost():
    form = CreatePostForm()
    if form.validate_on_submit():
        item = request.form['item']
        city = request.form['city']
        descrip = request.form['descrip']
        user_id = current_user.get_id()
        post = Posts(item, city, descrip, user_id)
        db.session.add(post)
        db.session.commit()
        #print('post valid')
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template("createpost.html", title="Create a New Post", form=form)
