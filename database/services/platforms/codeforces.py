import requests


def get_codeforces_user(handle):

    url = "https://codeforces.com/api/user.info"

    params = {
        "handles": handle
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    data = response.json()

    if data["status"] != "OK":
        raise Exception(data.get("comment", "Codeforces API error"))

    return data["result"][0]

def get_codeforces_submissions(handle):

    url = "https://codeforces.com/api/user.status"

    params = {
        "handle": handle
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data["status"] != "OK":
        raise Exception(
            data.get("comment", "Codeforces API error")
        )

    return data["result"]

def get_codeforces_stats(handle):

    submissions = get_codeforces_submissions(handle)

    total_submissions = len(submissions)

    accepted_submissions = 0
    solved_problems = set()

    for submission in submissions:

        if submission["verdict"] == "OK":

            accepted_submissions += 1

            problem = submission["problem"]

            problem_key = (
                problem.get("contestId"),
                problem.get("index")
            )

            solved_problems.add(problem_key)

    unique_problems_solved = len(solved_problems)

    return {
        "total_submissions": total_submissions,
        "accepted_submissions": accepted_submissions,
        "unique_problems_solved": unique_problems_solved
    }
    
def get_codeforces_rating_history(handle):

    url = "https://codeforces.com/api/user.rating"

    params = {
        "handle": handle
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data["status"] != "OK":
        raise Exception(
            data.get("comment", "Codeforces API error")
        )

    return data["result"]