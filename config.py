import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///campusforge.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CODEFORCES_CLIENT_ID = os.getenv("CODEFORCES_CLIENT_ID")
    CODEFORCES_CLIENT_SECRET = os.getenv("CODEFORCES_CLIENT_SECRET")