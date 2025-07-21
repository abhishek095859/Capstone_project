import json
import os
import subprocess

def rollback_cmd():
    print("===== Starting rollback...")

    key_path = "c:/Users/Minfy/Desktop/cli_tool/terraform/my-key.pem"
    config_file = ".vercelcli.json"
    deployment_file = ".vercel/deployments.json"

    if not os.path.exists(config_file):
        print("**** No .vercelcli.json found. Run `init` and `deploy` first.")
        return
    if not os.path.exists(deployment_file):
        print("**** No deployments found. Cannot rollback.")
        return

    # Load EC2 IP and user
    ssh_user = "ec2-user"
    with open(config_file) as f:
        config = json.load(f)
    ec2_ip = config.get("ec2_ip")

    if not ec2_ip:
        print("*** EC2 IP/DNS not found in config.")
        return

    # Load previous deployment
    with open(deployment_file) as f:
        deployments = json.load(f)

    if len(deployments) < 2:
        print("**** Not enough deployments to rollback.")
        return

    previous = deployments[-2]
    prev_tag = previous["tag"]
    print(f" Rolling back to: {prev_tag}")

    # SSH command to stop, remove, pull, and run
    ssh_command = f"""
    sudo docker ps -q | xargs -r sudo docker stop;
    sudo docker ps -a -q | xargs -r sudo docker rm;
    sudo docker pull {prev_tag};
    sudo docker run -d -p 80:80 {prev_tag};
    """

    try:
        subprocess.run([
            "ssh", "-i", key_path, f"{ssh_user}@{ec2_ip}",
            ssh_command
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"===== SSH command failed: {e}")
        return

    print(f"------ Successfully rolled back to {prev_tag}")
