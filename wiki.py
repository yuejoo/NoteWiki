import src
import datetime
from src import database
from src import forms as Forms
from src import models as DB_Models
from src import view as View
from src import login_manager
from flask import Flask, render_template, url_for, Markup, request, redirect, jsonify, flash, session, g
from flask import app as flask_app
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import markdown
from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')
    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value) for value in values)

fleet = src.config.FLEET_TEST
app = src.create_application(fleet)

SECRET_KEY = 'random_secret_key'
app.config['SECRET_KEY'] = SECRET_KEY
app.url_map.converters['list'] = ListConverter


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    user = DB_Models.User.query.filter_by(user_id=user_id).first()
    return user


@app.route('/home', methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = Forms.LoginForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user = DB_Models.User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            redirect_url = url_for('index')
            next = request.args.get('next')
            return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return render_template("home.html")


@app.route('/signup', methods=["GET", "POST"])
def register():
    form = Forms.RegisterForm(request.form, csrf_enabled=False)
    users = DB_Models.User.query.filter_by(email=form.email.data).all()
    if form.validate_on_submit():
        new_user = DB_Models.User(
            email=form.email.data,
            user_name=form.username.data,
            password=form.password.data,
            role_id=0
        )
        database.session.add(new_user)
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/view/<list:subs>', methods = ['GET'])
def view(subs):
    title = subs[-1]
    view = View.create_view_from_db(subs)

    return render_template("view.html", subs = subs, view = view)

@app.route('/edit/<list:subs>/delete', methods=['GET'])
@login_required
def edit_delete(subs):
    category_name = '+'.join(subs)
    View.delete_view_from_db(category_name)

    return render_template("home.html")

@app.route('/view/<list:subs>/delete', methods=['GET'])
@login_required
def view_delete(subs):
    category_name = '+'.join(subs)
    View.delete_view_from_db(category_name)

    return render_template("home.html")

@app.route('/edit/<list:subs>/save', methods=['POST'])
@login_required
def save(subs):
    title = request.form['title']
    content = request.form['content']
    category_name = '+'.join(subs)

    last_edited_by = current_user.user_name
    owner_id = current_user.id

    view = View.View(
        category_name = category_name,
        # Create view with empty html body for saving
        body = "",
        markdown_content = content,
        title = title,
        last_edited = datetime.datetime.now(),
        last_edited_by = last_edited_by,
        tags = []
    )

    View.persist_view_into_db(view)

    return jsonify(success=True)


@app.route('/edit/<list:subs>', methods = ['GET', 'POST'])
@login_required
def edit(subs):
    form = Forms.EditorForm(request.form)
    view = View.create_view_from_db(subs)
    return render_template("edit.html", subs = subs, view = view, form = form)

app.run(debug=True, threaded=True)