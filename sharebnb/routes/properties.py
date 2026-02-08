"""Property routes."""

from uuid import uuid4
from flask import Blueprint, render_template, jsonify, request
from sharebnb.models import db, Property, Image
from sharebnb.services import aws

properties_bp = Blueprint('properties', __name__)


@properties_bp.get("/")
def root():
    """TEST form."""
    return render_template("index.html")


@properties_bp.get('/properties')
def get_properties():
    """Returns all properties.
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


@properties_bp.post('/properties')
def add_property():
    """Add property,
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

    # cast to str to avoid test sqlite db error about UUID type
    aws_key = str(uuid4())

    image = Image(
        property_id=property.id,
        aws_key=aws_key,
        url=aws.generate_image_url(aws_key)
    )

    db.session.add(image)
    db.session.commit()

    aws.upload_image(property_image_file, image.aws_key)

    serialized = property.serialize()

    return (jsonify(property=serialized), 201)
