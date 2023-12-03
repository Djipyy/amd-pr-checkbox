import os
from typing import Tuple
from github import Github, PullRequest
from dotenv import load_dotenv

load_dotenv()


def handle_comment(comment: str, pr: PullRequest) -> Tuple[str, bool]:
    print("RAW COMMENT", comment)
    expected = f"- [] {pr.html_url}"
    expected_2 = f"- [ ] {pr.html_url}"

    out = comment.replace(expected, f"- [x] {pr.html_url}")
    out = out.replace(expected_2, f"- [x] {pr.html_url}")

    return out, out != comment


# def main():
#     gh_token = os.environ.get("PAT")
#     if gh_token is None:
#         raise Exception("Missing GitHub PAT")

#     g = Github(gh_token)

#     repo = g.get_repo("Djipyy/amd-test")
#     prs = repo.get_pulls()
#     for pr in prs:
#         issue = repo.get_issue(pr.number)
#         tl = issue.get_timeline()
#         for e in tl:
#             if (
#                 e.event == "cross-referenced"
#                 and e.source.issue.pull_request is not None
#             ):
#                 referenced_pr_id = e.source.issue.number
#                 referenced_pr_repo = e.source.issue.repository
#                 print("Reference repo", referenced_pr_repo.name)
#                 referenced_pr = referenced_pr_repo.get_pull(referenced_pr_id)
#                 print("Referenced PR : ", referenced_pr.title)
#                 print("URL", referenced_pr.html_url)
#                 for comment in referenced_pr.get_issue_comments():
#                     new, modifed = handle_comment(comment.body, pr)
#                     if modifed:
#                         try:
#                             comment.edit(new)
#                         except Exception as e:
#                             print("Couldn't edit comment", e)
#                         print("Edited comment", comment.html_url)
#                         print("New comment", new)
#                     else:
#                         print("No change")


def main():
    gh_token = os.environ.get("INPUT_PAT")
    if gh_token is None:
        raise ValueError("Missing GitHub PAT")

    g = Github(gh_token)

    print("GITHUB_ACTION_REPOSITORY", os.environ.get("GITHUB_ACTION_REPOSITORY"))
    print("INPUT_MERGING_PR_NUMBER", os.environ.get("INPUT_MERGING_PR_NUMBER"))
    print("INPUT_PAT", os.environ.get("INPUT_PAT"))
    repo = g.get_repo(os.environ.get("GITHUB_ACTION_REPOSITORY"))
    pr = repo.get_pull(int(os.environ.get("INPUT_MERGING_PR_NUMBER")))
    issue = repo.get_issue(pr.number)
    tl = issue.get_timeline()
    for e in tl:
        if e.event == "cross-referenced" and e.source.issue.pull_request is not None:
            referenced_pr_id = e.source.issue.number
            referenced_pr_repo = e.source.issue.repository
            print("Reference repo", referenced_pr_repo.name)
            referenced_pr = referenced_pr_repo.get_pull(referenced_pr_id)
            print("Referenced PR : ", referenced_pr.title)
            print("URL", referenced_pr.html_url)
            for comment in referenced_pr.get_issue_comments():
                new, modifed = handle_comment(comment.body, pr)
                if modifed:
                    try:
                        comment.edit(new)
                    except Exception as e:
                        print("Couldn't edit comment", e)
                    print("Edited comment", comment.html_url)
                    print("New comment", new)


if __name__ == "__main__":
    main()
