from datetime import datetime, timezone

from database import db
from database.models.platform_stats import PlatformStats

from database.services.platforms.codeforces import (
    get_codeforces_user,
    get_codeforces_stats
)


def sync_codeforces_account(account):

    user_data = get_codeforces_user(
        account.username
    )

    stats_data = get_codeforces_stats(
        account.username
    )

    platform_stats = PlatformStats.query.filter_by(
        platform_account_id=account.id
    ).first()

    if not platform_stats:

        platform_stats = PlatformStats(
            platform_account_id=account.id
        )

        db.session.add(platform_stats)

    platform_stats.total_submissions = (
        stats_data["total_submissions"]
    )

    platform_stats.accepted_submissions = (
        stats_data["accepted_submissions"]
    )

    platform_stats.unique_problems_solved = (
        stats_data["unique_problems_solved"]
    )

    platform_stats.rating = user_data.get("rating")

    platform_stats.max_rating = user_data.get("maxRating")

    platform_stats.rank = user_data.get("rank")

    platform_stats.last_synced = datetime.now(
        timezone.utc
    )

    db.session.commit()

    return platform_stats