import os
from dotenv import load_dotenv

from flask import (
    Flask, render_template, flash, redirect, session, g, abort, jsonify
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import (
    db, connect_db, User, Property, Image)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# Properties

@app.get('/properties')
def get_properties():
    """Returns all properties. 
            JSON like:
                { properties: [
                    {id, name, price, address, pool, backyard, images }], ...}
    """

    properties = Property.query.all()

    return jsonify(properties=properties)


