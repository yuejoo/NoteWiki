import src
import datetime
from src import models as DB_Models
from src import view as View
from flask import Flask, render_template, url_for, Markup, request, redirect, jsonify
from flask import app as flask_app
from flask_login import LoginManager, current_user
import markdown
from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')
    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
            for value in values)

fleet = src.config.FLEET_TEST
app = src.create_application(fleet)

app.url_map.converters['list'] = ListConverter

SECRET_KEY = 'random_secret_key'
app.config['SECRET_KEY'] = SECRET_KEY

print(app.root_path)

@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/view/<list:subs>', methods = ['GET'])
def view(subs):
    title = subs[-1]
    view = View.create_view_from_db(subs)

    return render_template("view.html", title = title, subs = subs, view = view)

@app.route('/edit/<list:subs>/save', methods=['POST'])
def save(subs):
    title = request.form['title']
    content = request.form['content']
    category_name = '+'.join(subs)

    last_edited_by = "Me"
    owner_id = 1
    tag_id = 1

    view = View.View(
        category_name = category_name,
        body = "",
        markdown_content = content,
        title = title,
        last_edited = datetime.datetime.now(),
        last_edited_by = last_edited_by,
        tags = []
    )

    View.persist_view_into_db(view)

    return jsonify(success=True)

from wtforms import SubmitField

@app.route('/edit/<list:subs>', methods = ['GET'])
def edit(subs):
    view = View.create_view_from_db(subs)
    return render_template("edit.html", title = "Title", subs = subs, view = view)

app.run()