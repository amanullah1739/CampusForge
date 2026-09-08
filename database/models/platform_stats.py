from database import db
from datetime import datetime


class PlatformStats(db.Model):

    __tablename__ = "platform_stats"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    platform_account_id = db.Column(
        db.Integer,
        db.ForeignKey("platform_accounts.id"),
        nullable=False,
        unique=True
    )

    total_submissions = db.Column(
        db.Integer,
        default=0
    )

    accepted_submissions = db.Column(
        db.Integer,
        default=0
    )

    unique_problems_solved = db.Column(
        db.Integer,
        default=0
    )

    rating = db.Column(
        db.Integer,
        nullable=True
    )

    max_rating = db.Column(
        db.Integer,
        nullable=True
    )

    rank = db.Column(
        db.String(100),
        nullable=True
    )

    last_synced = db.Column(
        db.DateTime,
        nullable=True
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

    def __repr__(self):
        return f"<PlatformStats {self.platform_account_id}>"