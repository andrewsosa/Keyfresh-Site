from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *

import pypugjs

# Init & Config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.url_map.strict_slashes = False
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

@pypugjs.register_filter('uppercase')
def uppercase(text, ast):
  return text.upper()

@pypugjs.register_filter('pug_href')
def pug_href(text):
  return "href={{url_for('static', filename='%s')}}" % text



# Init modules
bootstrap = Bootstrap(app)
db = MongoEngine(app)

from app import views
