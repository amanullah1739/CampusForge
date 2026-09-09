from database import db
from datetime import datetime


class College(db.Model):
    __tablename__ = "colleges"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    users = db.relationship(
        "User",
        back_populates="college",
        lazy=True
    )

    def __repr__(self):
        return f"<College {self.name}>"