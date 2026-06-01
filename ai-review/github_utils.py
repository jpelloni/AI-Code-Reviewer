import os
import json
from github import Github

def _load_event():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        raise RuntimeError("GITHUB_EVENT_PATH not set")
    with open(event_path, "r") as f:
        return json.load(f)

def get_pr_context():
    event = _load_event()
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = event["number"]
    return repo_name, pr_number

def get_pr_diff():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set")

    repo_name, pr_number = get_pr_context()
    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    diff_chunks = []
    for file in pr.get_files():
        if file.patch:
            diff_chunks.append(
                f"File: {file.filename}\nPatch:\n{file.patch}\n"
            )
    return "\n\n".join(diff_chunks)

def post_pr_comment(body: str):
    token = os.getenv("GITHUB_TOKEN")
    repo_name, pr_number = get_pr_context()
    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(body)