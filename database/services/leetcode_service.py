from datetime import datetime, timezone

from database import db
from database.models.platform_stats import PlatformStats

from database.services.platforms.leetcode import (
    get_leetcode_user
)


def sync_leetcode_account(account):

    data = get_leetcode_user(
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

    platform_stats.unique_problems_solved = (
        data["total_problems"]
    )
    platform_stats.easy_problems = data["easy"]
    
    platform_stats.medium_problems = data["medium"]
    
    platform_stats.hard_problems = data["hard"]

    platform_stats.rank = str(
        data["ranking"]
    )
    

    platform_stats.last_synced = datetime.now(
        timezone.utc
    )

    db.session.commit()

    return platform_stats