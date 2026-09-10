import requests


def get_leetcode_user(username):

    url = "https://leetcode.com/graphql/"

    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile {
                ranking
            }
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """

    variables = {
        "username": username
    }

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": variables
        },
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    user = data.get("data", {}).get("matchedUser")

    if not user:
        raise ValueError("LeetCode user not found.")

    problem_stats = {}

    for item in user["submitStats"]["acSubmissionNum"]:
        problem_stats[item["difficulty"]] = item["count"]

    return {
        "username": user["username"],
        "total_problems": problem_stats.get("All", 0),
        "easy": problem_stats.get("Easy", 0),
        "medium": problem_stats.get("Medium", 0),
        "hard": problem_stats.get("Hard", 0),
        "ranking": user["profile"]["ranking"]
    }