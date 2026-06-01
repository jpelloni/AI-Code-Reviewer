from github_utils import get_pr_diff, post_pr_comment
from llm_utils import review_diff_with_llm

def main():
    diff = get_pr_diff()
    if not diff.strip():
        post_pr_comment("AI review: No diff content found to review.")
        return

    review = review_diff_with_llm(diff)

    comment_body = (
        "## 🤖 AI Code Review\n\n"
        "_This is an automated review. Please treat it as a helper, not a gatekeeper._\n\n"
        f"{review}"
    )

    post_pr_comment(comment_body)

if __name__ == "__main__":
    main()