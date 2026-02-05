"""User model."""

from sharebnb.models.base import db


class User(db.Model):
    """Current users in the system."""

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

    def serialize(self):
        """Serialize property to a dict of property info."""

        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
