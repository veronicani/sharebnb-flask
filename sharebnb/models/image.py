"""Image model."""

from sharebnb.models.base import db


class Image(db.Model):
    """Current images for properties in the system."""

    __tablename__ = 'sbnb_images'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey('sbnb_properties.id', ondelete='CASCADE'),
        nullable=False,
    )

    storage_key = db.Column(
        db.String,
        nullable=False
    )

    url = db.Column(
        db.String,
        nullable=False,
    )

    def serialize(self):
        """Serialize property to a dict of property info."""

        return {
            "id": self.id,
            "property_id": self.property_id,
            "storage_key": self.storage_key,
            "url": self.url,
        }
