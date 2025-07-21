from internal.git import clone_repo
from internal.detect import detect_stack
from internal.build import build_project
from internal.build import write_dockerfile

def deploy_from_repo(repo_url):
    print(f"------ Cloning {repo_url}...")
    repo_path = clone_repo(repo_url)
    if not repo_path:
        print("+++++++ Aborting deployment due to clone failure.")
        return


    stack, app_path = detect_stack(repo_path)
    print(f"-------- Detected stack: {stack}")

    build_path = build_project(app_path, stack)
    print(f"----- Build output at: {build_path}")

    

