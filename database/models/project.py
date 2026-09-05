from database import db
from datetime import datetime


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    github_url = db.Column(
        db.String(255),
        nullable=True
    )

    live_url = db.Column(
        db.String(255),
        nullable=True
    )

    tech_stack = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(50),
        default="Completed"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Project {self.title}>"