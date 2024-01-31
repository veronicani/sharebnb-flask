"""SQLAlchemy models for shareBnB."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Property(db.Model):
    """Current properties in the system. """

    __tablename__ = 'properties'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    address = db.Column(
        db.String(50),
        nullable=False,
    )

    price = db.Column(
        db.Integer,
        nullable=False,
    )

    backyard = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    pool = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    images = db.relationship('Image', backref="property")
    # backref'ed in User Model
    # user = db.relationship('Property', backref="properties")


class User(db.Model):
    """Current users in the system. """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
    )

    properties = db.relationship('Property', backref="user")


class Image(db.Model):
    """Current images for properties in the system."""

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    properties_id = db.Column(
        db.Integer,
        db.ForeignKey('properties.id', ondelete='CASCADE'),
        nullable=False,
    )

    # backref'd in Property Model
    # property = db.relationship('Property', backref="images")