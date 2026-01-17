import sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import pprint
import json

if len(sys.argv) < 2:
    print("Uso correto do comando: python github_activity.py <username>")
    sys.exit(1)

username = sys.argv[1]

# --------------------------------------
# Fetchs
# --------------------------------------


def fetch_github_user_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urlopen(url) as response:
            return json.loads(response.read())

    except HTTPError as e:
        if e.code == 404:
            print("Usuário não encontrado")
        else:
            print(f"Erro HTTP: {e.code}")
    except URLError:
        print("Erro de conexão com a internet")

    return []


def fetch_github_user_repo_commits(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    try:
        with urlopen(url) as response:
            commits = json.loads(response.read())
            return len(commits)

    except HTTPError:
        return 0
    except URLError:
        return 0


def fetch_github_user_repo_issues(repo):
    url = f"https://api.github.com/repos/{repo}/issues"

    try:
        with urlopen(url) as response:
            return json.loads(response.read())
    except HTTPError:
        return []
    except URLError:
        return []


processed = {
    "PushEvent": set(),
    "IssuesEvent": set(),
    "WatchEvent": set(),
}

repo_cache = {
    "commits": {},
    "issues": {},
}

# --------------------------------------
# Events
# --------------------------------------


def handle_event(event):
    event_type = event["type"]
    repo = event["repo"]["name"]

    if event_type == "IssueCommentEvent":
        return handle_issue_comment_event(event)

    if event_type not in processed:
        return f"{event_type} in repo"

    if repo in processed[event_type]:
        return None

    processed[event_type].add(repo)

    if event_type == "PushEvent":
        return handle_push_event(repo)

    if event_type == "IssueEvent":
        action = event["payload"]["action"]
        return f"{action.capitalize()} an issue in {repo}"

    if event_type == "WatchEvent":
        return f"Starred {repo}"


# --------------------------------------
# Events
# --------------------------------------


def handle_push_event(repo):
    if repo not in repo_cache["commits"]:
        repo_cache["commits"][repo] = fetch_github_user_repo_commits(
            username, repo.split("/")[1]
        )

    commits = repo_cache["commits"][repo]
    return f"Pushed {commits} commits to {repo}"


def handle_issue_comment_event(event):
    repo = event["repo"]["name"]

    if repo not in repo_cache["issues"]:
        repo_cache["issues"][repo] = fetch_github_user_repo_issues(repo)

    issues = repo_cache["issues"][repo]

    if not issues:
        return f"IssueCommentEvent in {repo} (no issues found)"

    messages = []
    for issue in issues[:3]:
        messages.append(f"Issue #{issue['number']}: {issue['title']}")

    return f"IssueCommentEvent in {repo}\n" + "\n".join(messages)


events = fetch_github_user_activity(username)

for event in events:
    message = handle_event(event)
    if message:
        print(" - ", message)
