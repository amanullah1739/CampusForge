from datetime import datetime, timezone

from database import db
from database.models.gfg_stats import GFGStats

from database.services.platforms.gfg import (
    get_gfg_basic_stats
)


def sync_gfg_account(account):

    stats_data = get_gfg_basic_stats(
        account.username
    )

    gfg_stats = GFGStats.query.filter_by(
        platform_account_id=account.id
    ).first()

    if not gfg_stats:

        gfg_stats = GFGStats(
            platform_account_id=account.id
        )

        db.session.add(gfg_stats)

    gfg_stats.problems_solved = (
        stats_data["problems_solved"]
    )

    gfg_stats.coding_score = (
        stats_data["coding_score"]
    )

    gfg_stats.rank = (
        stats_data["rank"]
    )

    gfg_stats.last_synced = (
        datetime.now(timezone.utc)
    )

    db.session.commit()

    return gfg_stats