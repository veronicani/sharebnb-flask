import os
from dotenv import load_dotenv

from flask import (
    Flask, render_template, flash, redirect, session, g, abort, jsonify, request
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
    """ Returns all properties.
            JSON like:
                { properties: [
                    {id, name, price, address, pool, backyard, images }], ...}
    """

    search = request.args.get("term")

    if not search:
        properties = Property.query.all()
    else:
        properties = Property.query.filter(Property.name.ilike(f"%search%")).all()

    serialized = [property.serialize() for property in properties]


    return jsonify(properties=serialized)

@app.post('/properties')
def add_property():
    """ Add property,
            {name, description, address, price, backyard, pool, images}
        Returns confirmation message.
    """

    data = request.json

    # TODO: research on AWS uploading images
    property = Property(
        name=data['name'],
        description=data['description'],
        address=data['address'],
        price=data['price'],
        backyard=data['backyard'],
        pool=data['pool'],
        images=data['images']
    )

    db.session.add(property)
    db.session.commit()

    serialized = property.serialize()

    return (jsonify(property=serialized), 201)




