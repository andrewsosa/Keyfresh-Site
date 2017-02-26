from app import app

from flask_nav import Nav
from flask_nav.elements import *


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
