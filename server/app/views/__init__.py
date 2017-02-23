from flask import redirect, url_for, render_template, request, session
from flask_nav import Nav
from flask_nav.elements import *

import bleach, re

from app import app, db
from app.models import Account

# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


# Nav bar
topbar = Navbar('',
    Link('Home', '/'),
    Link('FAQ','/#faq'),
        Link('Sponsors', '/#sponsors'),
        Link('Register', '/register'),
        Link('Login','/login'),
)

nav = Nav()
nav.register_element('top', topbar)
nav.init_app(app)


# Routes
@app.route('/')
def index():
    return render_template('index.html')
