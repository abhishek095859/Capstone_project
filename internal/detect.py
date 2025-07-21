import os
import json

def detect_stack(repo_path):
    """
    Recursively detects whether the project is:
    - React (CRA)
    - Vite
    - HTML (index.html only)
    """

    for dirpath, dirs, files in os.walk(repo_path):
        if "package.json" in files:
            pkg_path = os.path.join(dirpath, "package.json")
            with open(pkg_path) as f:
                pkg = json.load(f)

            deps = pkg.get("dependencies", {})
            dev_deps = pkg.get("devDependencies", {})
            all_deps = {**deps, **dev_deps}

            if "vite" in all_deps:
                print(f"---- Detected Vite in {dirpath}")
                return "vite", dirpath

            if "react-scripts" in all_deps:
                print(f"----- Detected CRA React in {dirpath}")
                return "react", dirpath

        if "index.html" in files and "package.json" not in files:
            print(f"----- Detected HTML app in {dirpath}")
            return "html", dirpath

    raise Exception("******* Unable to detect tech stack.")
