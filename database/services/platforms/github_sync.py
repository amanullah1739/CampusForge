from datetime import datetime, timezone

from database import db
from database.models.github_stats import GitHubStats

from database.services.platforms.github import (
    get_github_basic_stats
)


def sync_github_account(account):

    stats_data = get_github_basic_stats(
        account.username
    )

    github_stats = GitHubStats.query.filter_by(
        platform_account_id=account.id
    ).first()

    if not github_stats:

        github_stats = GitHubStats(
            platform_account_id=account.id
        )

        db.session.add(github_stats)

    github_stats.public_repositories = (
        stats_data["public_repositories"]
    )

    github_stats.stars = (
        stats_data["stars"]
    )

    github_stats.forks = (
        stats_data["forks"]
    )

    github_stats.repository_count = (
        stats_data["repository_count"]
    )

    github_stats.last_synced = (
        datetime.now(timezone.utc)
    )

    db.session.commit()

    return github_stats