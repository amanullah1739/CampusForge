from database import db
from datetime import datetime


class GFGStats(db.Model):

    __tablename__ = "gfg_stats"

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

    problems_solved = db.Column(
        db.Integer,
        default=0
    )

    coding_score = db.Column(
        db.Integer,
        default=0
    )

    rank = db.Column(
        db.Integer,
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

        return f"<GFGStats {self.platform_account_id}>"