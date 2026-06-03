# AI Code Reviewer

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

AI Code Reviewer automates pull request feedback using GitHub metadata, PR diffs, custom review rules, and an OpenAI model.

It is designed as a helper for human reviewers, not as a merge gate.

## What It Does

For each pull request run, the reviewer:

1. Reads pull request context from the GitHub Actions event payload.
2. Fetches changed-file patches with the GitHub API.
3. Sends the diff plus optional custom rules to the LLM.
4. Posts a markdown review comment back to the PR.

## Repository Structure

```text
.
├── .github/workflows/ai-code-review.yml
├── ai-review/
│   ├── github_utils.py
│   ├── llm_utils.py
│   ├── reviewer.py
│   └── rules_loader.py
├── action.yml
├── Dockerfile
├── requirements.txt
└── .api-review-rules.yml
```

## Tech Stack

- Python 3.11+
- PyGithub
- OpenAI Python SDK
- PyYAML
- Requests (dependency utility)

## Configuration

### Required Environment Variables

| Variable | Description |
| --- | --- |
| `GITHUB_TOKEN` | Token used to read pull request files and post a PR comment. In GitHub Actions, use `${{ secrets.GITHUB_TOKEN }}`. |
| `GITHUB_REPOSITORY` | Repository slug in `owner/repo` format. Provided automatically in Actions. |
| `GITHUB_EVENT_PATH` | Path to event payload JSON. Provided automatically in Actions. |
| `OPENAI_API_KEY` | OpenAI API key used to generate review feedback. |

### Optional Rules File

You can define project-specific review rules in `.api-review-rules.yml`.

Example:

```yaml
style:
  - Prefer async/await over callbacks.
security:
  - Validate all external inputs.
tests:
  - Every new feature must include at least one unit test.
```

Rules are flattened into a single list and included in the LLM prompt.

## Run In GitHub Actions

This repository already contains a ready-to-run workflow at `.github/workflows/ai-code-review.yml`.

It triggers on PR open/update/reopen and runs:

```bash
python ai-review/reviewer.py
```

### Required Repository Secret

- `OPENAI_API_KEY`

`GITHUB_TOKEN` is supplied automatically by GitHub Actions.

## Run Locally

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set required environment variables

```bash
export GITHUB_TOKEN="<your-github-token>"
export OPENAI_API_KEY="<your-openai-api-key>"
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_EVENT_PATH="$(pwd)/event.json"
```

### 4. Create a minimal event payload

```bash
cat > event.json << 'EOF'
{
  "number": 1
}
EOF
```

### 5. Run the reviewer

```bash
python ai-review/reviewer.py
```

If successful, the script posts a PR comment titled `## 🤖 AI Code Review`.

## GitHub Action Metadata

The repository includes a Docker-based action definition in `action.yml` and `Dockerfile`.

If you use the action directly in another workflow, ensure `OPENAI_API_KEY` is available to the container environment in addition to the declared action input.

## Notes And Limits

- Large diffs are truncated to 12,000 characters before sending to the LLM.
- Files without patch content are skipped.
- The current LLM model in code is `gpt-4o-mini`.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
