# internal/git

import subprocess
import tempfile

def clone_repo(repo_url):
    """
    Clones a GitHub repo to a temporary directory.
    Returns the local path or None on failure.
    """
    temp_dir = tempfile.mkdtemp(prefix="repo_")
    print(f"+++++ Cloning into: {temp_dir}")

    try:
        subprocess.check_call(['git', 'clone', repo_url, temp_dir])
        print("+++++++ Repo cloned successfully!")
        return temp_dir
    except subprocess.CalledProcessError as e:
        print("** Clone failed:", e)
        return None
