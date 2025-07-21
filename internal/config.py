# File: internal/config/init_setup.py

import os
import json
from internal.detect import detect_stack

def detect_and_configure_project():
    print("...... Detecting project type...")

    try:
        # Detect stack from current working directory
        stack, path = detect_stack(os.getcwd())

        config = {
            "project_type": stack,
            "project_root": path
        }

        # Save config to deployment_config.json
        config_path = os.path.join(os.getcwd(), "deployment_config.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"^^^^^^ Project type: {stack}")
        print(f"<><> Config saved at: {config_path}")
        return config

    except Exception as e:
        print("----- Could not detect project type:", e)
        return None
    
def get_config():
    config_path = os.path.join(os.getcwd(), "deployment_config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(" Config file not found. Run `init` first.")
    with open(config_path, "r") as f:
        return json.load(f)
