from database import db
from datetime import datetime


class UserSkill(db.Model):

    __tablename__ = "user_skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    skill = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="skills"
    )

    def __repr__(self):
        return f"<UserSkill {self.skill}>"