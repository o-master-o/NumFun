from git import Repo
from git.exc import GitCommandError


def update_git_repo(repo_path):
    try:
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.fetch()
        current_branch = repo.active_branch
        repo.head.reset('origin/' + current_branch.name, index=True, working_tree=True)

        print(f"Repository at {repo_path} successfully updated.")
        return True
    except GitCommandError as e:
        print(f"An error occurred while updating the repository: {e}")
        return False
