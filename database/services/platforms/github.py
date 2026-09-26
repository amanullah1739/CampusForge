import requests


GITHUB_API = "https://api.github.com"


def github_request(endpoint, params=None):

    url = f"{GITHUB_API}{endpoint}"

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_github_user(username):

    return github_request(
        f"/users/{username}"
    )


def get_github_repositories(username):

    repositories = []

    page = 1

    while True:

        data = github_request(
            f"/users/{username}/repos",
            params={
                "per_page": 100,
                "page": page,
                "type": "all"
            }
        )

        if not data:
            break

        repositories.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repositories


def get_github_basic_stats(username):

    user = get_github_user(username)

    repositories = get_github_repositories(
        username
    )

    public_repositories = sum(
        1
        for repo in repositories
        if not repo.get("private", False)
    )

    stars = sum(
        repo.get("stargazers_count", 0)
        for repo in repositories
    )

    forks = sum(
        repo.get("forks_count", 0)
        for repo in repositories
    )

    return {
        "public_repositories": public_repositories,
        "stars": stars,
        "forks": forks,
        "repository_count": len(repositories)
    }
    
def validate_github_username(username):

    try:

        user = get_github_user(username)

        return user

    except requests.HTTPError as e:

        if e.response is not None and e.response.status_code == 404:
            return None

        raise
    
