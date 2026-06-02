# AI Code Reviewer

[![Python](https://img.shields.io/badge/python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

AI Code Reviewer is a Python project for automating pull request feedback with LLM-assisted review workflows.

The repository combines:
- A Flask API starter app for local development and extension.
- Core review utilities for GitHub PR diff retrieval and LLM-based analysis.
- A lightweight foundation you can evolve into a production review assistant.

## Why This Project

Manual PR review takes time and can miss repetitive issues. This project is designed to help by:
- Pulling PR diffs from GitHub.
- Sending code changes to an LLM for analysis.
- Posting review feedback back to the PR.

It is intended as an assistant, not a gatekeeper.

## Current Features

- Flask app factory pattern for clean app setup.
- Health endpoint for service readiness checks.
- Starter users controller endpoint for API scaffolding.
- Python utility modules for GitHub and LLM review flows under the ai-review folder.

## Project Status

This is an early-stage starter project. The API and review modules are intentionally simple so they are easy to extend.

## Tech Stack

- Python 3.14+
- Flask
- PyGithub
- OpenAI SDK
- Requests / HTTPX
- PyYAML

## Project Structure

```text
.
├── ai-review/
│   ├── github_utils.py
│   ├── llm_utils.py
│   ├── reviewer.py
│   └── rules_loader.py
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   └── controllers/
│   │       ├── __init__.py
│   │       └── users_controller.py
│   └── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Code-Reviewer.git
cd AI-Code-Reviewer
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Flask App

```bash
python ./src/main.py
```

The app starts on http://0.0.0.0:5000.

## Quickstart: Run the Reviewer Flow

The review runner lives in ai-review/reviewer.py and expects GitHub Actions style context.

### 1. Set environment variables

```bash
export GITHUB_TOKEN="<your-github-token>"
export OPENAI_API_KEY="<your-openai-api-key>"
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_EVENT_PATH="$(pwd)/event.json"
```

### 2. Create a minimal event payload

```bash
cat > event.json << 'EOF'
{
  "number": 1
}
EOF
```

### 3. Run the reviewer

```bash
cd ai-review
python reviewer.py
```

If successful, the script reads the PR diff, requests an LLM review, and posts a comment to the pull request.

## GitHub Actions Setup

This repository already includes a workflow at `.github/workflows/ai-code-review.yml` that runs on pull request events.

Add this repository secret before enabling the workflow:
- `OPENAI_API_KEY`

Notes:
- `GITHUB_TOKEN` is provided automatically by GitHub Actions.
- `GITHUB_REPOSITORY` and `GITHUB_EVENT_PATH` are available in the Actions runtime and are consumed by the reviewer utilities.

Use the existing workflow file directly and edit it as needed for your repository.

Customize this in `.github/workflows/ai-code-review.yml`:
- Trigger events under `on:`.
- Python version under `actions/setup-python`.
- Dependency install strategy (for example lockfiles or cache).
- Job permissions if your org requires stricter defaults.

## API Endpoints

### GET /health

Basic health check endpoint.

Example response:

```json
{
  "status": "ok"
}
```

### GET /users

Starter controller endpoint returning in-memory users.

Example response:

```json
{
  "users": [
    {
      "id": 1,
      "name": "Starter User",
      "email": "starter@example.com"
    }
  ]
}
```

## Review Automation Modules

The ai-review folder contains the building blocks for PR automation:
- github_utils.py: fetches PR diffs and posts PR comments.
- llm_utils.py: sends diff content to an LLM for review.
- reviewer.py: orchestration script for running review flow end-to-end.
- rules_loader.py: loads configurable review rules.

## Configuration

### Required Environment Variables

| Variable | Required | Used In | Description |
| --- | --- | --- | --- |
| `GITHUB_TOKEN` | Yes | ai-review/github_utils.py | GitHub token used to read pull requests and post comments. |
| `GITHUB_REPOSITORY` | Yes | ai-review/github_utils.py | Repository in `owner/repo` format. |
| `GITHUB_EVENT_PATH` | Yes | ai-review/github_utils.py | Path to JSON event payload containing PR metadata (uses `number`). |
| `OPENAI_API_KEY` | Yes | ai-review/llm_utils.py | API key used for LLM-based review generation. |

### Optional Rules File

You can define additional review rules in a YAML file named `.api-review-rules.yml`.

Example:

```yaml
security:
  - Validate all external input.
testing:
  - Call out missing unit tests for new logic.
```

## Roadmap Ideas

- Add persistent storage for users and review history.
- Add authentication and role-based access.
- Expose review execution via Flask endpoints.
- Add unit tests and CI checks.
- Add Docker support for deployment.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
