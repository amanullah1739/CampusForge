from database import db
from datetime import datetime


class User(db.Model):

    __tablename__ = "users"

    # =========================================
    # PRIMARY KEY
    # =========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================================
    # BASIC INFORMATION
    # =========================================

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    roll_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    branch = db.Column(
        db.String(50),
        nullable=False
    )

    year = db.Column(
        db.String(20),
        nullable=False
    )

    # =========================================
    # AUTHENTICATION
    # =========================================

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # =========================================
    # GAMIFICATION
    # =========================================

    total_xp = db.Column(
        db.Integer,
        default=0
    )

    streak = db.Column(
        db.Integer,
        default=0
    )

    # =========================================
    # ACCOUNT INFORMATION
    # =========================================

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

        return f"<User {self.email}>"