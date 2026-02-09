"""Property routes."""

from uuid import uuid4
from flask import Blueprint, render_template, jsonify, request
from sharebnb.models import db, Property, Image
from sharebnb.services import storage

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
    required_fields = ['name', 'description', 'address', 'price']

    for field in required_fields:
        if field not in data:
            return jsonify(error=f"Missing required field: {field}"), 400

    prop_img_fn = request.files.get('image')
    if not prop_img_fn:
        return jsonify(error="Image file is required"), 400
    
    try:
        new_prop = Property(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            price=data['price'],
            backyard=True if data['backyard'] == 'true' else False,
            pool=True if data['pool'] == 'true' else False,
            user_id=1
        )

        db.session.add(new_prop)
        # Flush to get new_prop.id before commit, needed for image record
        db.session.flush()

        # cast to str to avoid test sqlite db error about UUID type
        img_key = str(uuid4())
        new_img = Image(
            property_id=new_prop.id,
            storage_key=img_key,
            url=storage.generate_image_url(img_key)
        )

        db.session.add(new_img)

        upload_success = storage.upload_image(prop_img_fn, new_img.storage_key)
        if not upload_success:
            return jsonify(error="Failed to upload image"), 500 
        
        db.session.commit()

        serialized = new_prop.serialize()
        return (jsonify(property=serialized), 201)
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
