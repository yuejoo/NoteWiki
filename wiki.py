from flask import Flask, render_template, url_for, Markup, request
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

login_manager = LoginManager()

app = Flask(__name__)

app.url_map.converters['list'] = ListConverter

login_manager.init_app(app)

SECRET_KEY = 'random_secret_key'
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/view/<list:subs>', methods = ['GET', 'POST'])
def view(subs):
    title = subs[-1]
    return render_template("view.html", title = title, subs = subs)

@app.route('/edit/<list:subs>', methods = ['GET', 'POST'])
def edit(subs):
    title = subs[-1]
    return render_template("edit.html", title = title, subs = subs)

app.run()