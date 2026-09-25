from database import db
from datetime import datetime


class GitHubStats(db.Model):

    __tablename__ = "github_stats"

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

    public_repositories = db.Column(
        db.Integer,
        default=0
    )

    stars = db.Column(
        db.Integer,
        default=0
    )

    forks = db.Column(
        db.Integer,
        default=0
    )

    contributions = db.Column(
        db.Integer,
        default=0
    )

    commits = db.Column(
        db.Integer,
        default=0
    )

    pull_requests = db.Column(
        db.Integer,
        default=0
    )

    issues = db.Column(
        db.Integer,
        default=0
    )

    repository_count = db.Column(
        db.Integer,
        default=0
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
        return f"<GitHubStats {self.platform_account_id}>"