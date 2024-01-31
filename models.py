"""SQLAlchemy models for shareBnB."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Properties(db.Model):
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
        default="",
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

