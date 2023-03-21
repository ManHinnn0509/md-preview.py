import requests as req

def send_request(content: str, token: str):
    url = "https://api.github.com/markdown"

    h = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    b = {
        "text": content
    }

    r = req.post(url, headers=h, json=b)
    if (r.status_code != 200):
        return None

    return r.text
    # return r.content.decode("utf-8")


def read_file(p: str, encoding='utf-8'):
    try:
        with open(p, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return None
