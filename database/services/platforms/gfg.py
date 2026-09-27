import requests
import re


def get_gfg_profile(username):

    url = f"https://www.geeksforgeeks.org/user/{username}/"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.text

def get_gfg_basic_stats(username):

    html = get_gfg_profile(username)

    score_match = re.search(
        r'\\"score\\":(\d+)',
        html
    )

    problems_match = re.search(
        r'\\"total_problems_solved\\":(\d+)',
        html
    )

    rank_match = re.search(
        r'\\"institute_rank\\":\\"(\d*)\\"',
        html
    )

    coding_score = (
        int(score_match.group(1))
        if score_match
        else 0
    )

    problems_solved = (
        int(problems_match.group(1))
        if problems_match
        else 0
    )

    rank = None

    if rank_match and rank_match.group(1):
        rank = int(rank_match.group(1))

    print(
        "GFG PARSED:",
        problems_solved,
        coding_score,
        rank
    )

    return {
        "problems_solved": problems_solved,
        "coding_score": coding_score,
        "rank": rank
    }