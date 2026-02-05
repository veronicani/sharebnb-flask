"""Property model."""

from sharebnb.models.base import db


class Property(db.Model):
    """Current properties in the system."""

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

    def serialize(self):
        """Serialize property to a dict of property info."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "price": self.price,
            "backyard": self.backyard,
            "pool": self.pool,
            "user_id": self.user_id,
            "images": [image.serialize() for image in self.images],
        }
