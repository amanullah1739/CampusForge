from app import app
from database import db
from database.models.user import User
from database.models.project import Project
from database.models.platform_account import PlatformAccount
from database.models.platform_stats import PlatformStats


with app.app_context():

    # Delete platform stats first
    PlatformStats.query.delete()

    # Delete platform accounts
    PlatformAccount.query.delete()

    # Delete projects
    Project.query.delete()

    # Delete users
    User.query.delete()

    db.session.commit()

    print("All users and related data deleted successfully.")