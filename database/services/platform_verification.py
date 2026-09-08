import secrets
import string
from datetime import datetime, timedelta


def generate_verification_code():

    characters = string.ascii_uppercase + string.digits

    code = "".join(
        secrets.choice(characters)
        for _ in range(8)
    )

    return f"CF-{code}"


def get_verification_expiry():

    return datetime.utcnow() + timedelta(minutes=15)