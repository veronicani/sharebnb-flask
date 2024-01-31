import os
from dotenv import load_dotenv
import boto3

from flask import (
    Flask, render_template, flash, redirect, session, g, abort, jsonify, request
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import (
    db, connect_db, User, Property, Image)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sharebnb')
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'secret')

toolbar = DebugToolbarExtension(app)

connect_db(app)
###############################################################################
# global variables

AWS_BUCKET = os.environ['AWS_BUCKET']
print("AWS_BUCKET=", AWS_BUCKET)

S3 = boto3.client(
    "s3",
    os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)
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
            Property.name.ilike(f"%search%")).all()

    serialized = [property.serialize() for property in properties]

    return jsonify(properties=serialized)


@app.post('/')
def add_property():
    """ Add property,
            {name, description, address, price, backyard, pool, images}
        Returns confirmation message.
    """

    data = request.form
    # save object(image_file) name in database
    breakpoint

    S3.upload_file("./test_img/pool1.jpg",
                   AWS_BUCKET,
                   "pool1.jpg")

    property = Property(
        name=data['name'],
        description=data['description'],
        address=data['address'],
        # price=data['price'],
        # backyard=data['backyard'],
        # pool=data['pool'],
        # images=data['images']
    )

    property_image = data['image']

    print("property=", property)
    print("image file=",property_image)

    db.session.add(property)
    db.session.commit()

    serialized = property.serialize()

    return (jsonify(property=serialized), 201)

# TODO: make AWS accounts! And try to upload images through test form


# print('Existing buckets: ')
# for bucket in response['Buckets']:
#     print(f'{bucket["Name"]}')
