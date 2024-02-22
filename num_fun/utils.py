from pathlib import Path

from git import Repo
from git.exc import GitCommandError

REPO_PATH = Path(__file__).parents[1]


def update_git_repo():
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remotes.origin
        origin.fetch()
        current_branch = repo.active_branch
        repo.head.reset('origin/' + current_branch.name, index=True, working_tree=True)

        print(f"Repository at {REPO_PATH} successfully updated.")
        return True
    except GitCommandError as e:
        print(f"An error occurred while updating the repository: {e}")
        return False
