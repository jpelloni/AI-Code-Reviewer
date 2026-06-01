import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a senior software engineer doing code review.
You:
- Focus on correctness, security, readability, and test coverage.
- Are concise and specific.
- Only comment on meaningful issues; avoid nitpicks.
Return your feedback as markdown with bullet points and code blocks where helpful.
"""

def review_diff_with_llm(diff: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)

    # Truncate if diff is huge (simple safeguard)
    max_chars = 12000
    if len(diff) > max_chars:
        diff = diff[:max_chars] + "\n\n[Diff truncated for review]"

    user_prompt = f"""Review the following pull request diff.

Provide:
- A short summary of the change.
- 3–10 concrete review comments.
- Call out missing tests or risky areas.

Diff:
{diff}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return resp.choices[0].message.content.strip()