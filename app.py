import os

from uuid import uuid4
from flask_cors import CORS
from flask import (
    Flask, render_template, jsonify, request
)
from flask_debugtoolbar import DebugToolbarExtension
from aws import upload_image, generate_image_url
from models import (
    db, connect_db, Property, Image)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sharebnb')
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'secret')

toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# TEST form at root, so we can try our POST route and see if AWS works


@app.get("/")
def root():
    """TEST form."""

    return render_template("index.html")


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
        properties = Property.query.filter(
            Property.name.ilike(f"%{search}%")).all() or Property.query.filter(
                Property.address.ilike(f"%{search}%")).all()

    serialized = [property.serialize() for property in properties]

    return jsonify(properties=serialized)


@app.post('/properties')
def add_property():
    """ Add property,
            {name, description, address, price, backyard, pool, images}
        Returns confirmation message.
    """

    data = request.form

    property = Property(
        name=data['name'],
        description=data['description'],
        address=data['address'],
        price=data['price'],
        backyard=True if data['backyard'] == 'true' else False,
        pool=True if data['pool'] == 'true' else False,
        user_id=1
    )

    property_image_file = request.files['image']

    db.session.add(property)
    db.session.commit()

    aws_key = uuid4()

    image = Image(
        property_id=property.id,
        aws_key=aws_key,
        url=generate_image_url(aws_key)
    )

    db.session.add(image)
    db.session.commit()

    upload_image(property_image_file, image.aws_key)

    serialized = property.serialize()

    return (jsonify(property=serialized), 201)

