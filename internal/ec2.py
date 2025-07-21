import subprocess
import time
import json

def deploy_to_ec2(image_name, username, repo, token, key_path, dockerfile_dir):
    tag = f"{username}/{repo}:{int(time.time())}"

    # Build and push image
    subprocess.run(["docker", "build", "-t", tag, dockerfile_dir], check=True)
    subprocess.run(["docker", "login", "-u", username, "-p", token], check=True)
    subprocess.run(["docker", "push", tag], check=True)

    # Read EC2 IP
    with open("terraform/output.json") as f:
        outputs = json.load(f)
    ec2_ip = outputs["public_ip"]["value"]

    # Pull image on EC2
    subprocess.run([
        "ssh", "-o", "StrictHostKeyChecking=no", "-i", key_path, f"ec2-user@{ec2_ip}",
        f"sudo docker pull {tag}"
    ], check=True)

    # Run image on EC2
    subprocess.run([
    "ssh", "-o", "StrictHostKeyChecking=no", "-i", key_path, f"ec2-user@{ec2_ip}",
    f"""
    sudo docker ps -q --filter 'publish=80' | xargs -r sudo docker rm -f;
    sudo docker run -d -p 80:80 {tag}
    """
], check=True)


    print(f" -------Deployment complete. App live at http://{ec2_ip}")
    return ec2_ip

def monitoring_set(key_path, ec2_ip):
    print(f"---------- Monitoring is live at:\n - Prometheus: http://{ec2_ip}:9090\n - Grafana: http://{ec2_ip}:3000\n - nodeexporter: http://{ec2_ip}:9100\n")
