from database import db
from datetime import datetime


class PlatformAccount(db.Model):

    __tablename__ = "platform_accounts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    platform = db.Column(
        db.String(50),
        nullable=False
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    profile_url = db.Column(
        db.String(255),
        nullable=True
    )

    verified = db.Column(
        db.Boolean,
        default=False
    )
    
    verification_code = db.Column(
    db.String(20),
    nullable=True
    )

    verification_expires_at = db.Column(
        db.DateTime,
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
        return f"<PlatformAccount {self.platform}: {self.username}>"