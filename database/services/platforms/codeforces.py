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