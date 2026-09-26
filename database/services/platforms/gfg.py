import requests
from bs4 import BeautifulSoup


def get_gfg_profile(username):

    url = f"https://www.geeksforgeeks.org/user/{username}/"

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    return response.text


def get_gfg_basic_stats(username):

    html = get_gfg_profile(username)

    def extract_value(key):

        marker = f'\\"{key}\\":'

        index = html.find(marker)

        if index == -1:
            return None

        start = index + len(marker)

        end = html.find(",", start)

        if end == -1:
            end = html.find("}", start)

        value = html[start:end].strip()

        value = value.strip('"')

        return value

    problems_solved = extract_value(
        "total_problems_solved"
    )

    score = extract_value(
        "score"
    )

    institute_rank = extract_value(
        "institute_rank"
    )

    return {
        "problems_solved": int(
            problems_solved or 0
        ),
        "coding_score": int(
            score or 0
        ),
        "rank": institute_rank or None
    }