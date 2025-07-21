import click
import json
import os
import time
from internal.git import clone_repo
from internal.detect import detect_stack
from internal.build import write_dockerfile
from internal.s3 import upload_folder_to_s3
from internal.aws import provision_infrastructure
from internal.ec2 import deploy_to_ec2, monitoring_set
from internal.rollback import rollback_cmd
from internal.destroy import destroy_ec2

DEPLOYMENTS_FILE = ".vercel/deployments.json"
CONFIG_FILE = ".vercelcli.json"

@click.group()
def cli():
    pass

@cli.command()
def init():
    click.echo("🎉 Welcome to Mini Vercel!")

    repo_url = click.prompt(" Enter your GitHub repository URL :--")
    repo_path = clone_repo(repo_url)
    stack, app_path = detect_stack(repo_path)

    upload_folder_to_s3(repo_path, bucket_name="mini-vercel", s3_prefix="", profile_name="my-sso")

    metadata = {
        "repo_url": repo_url,
        "stack": stack,
        "app_path": app_path
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

    click.echo(" ^^^^ Project initialized. ^^^^")

@cli.command()
def deploy():
    click.echo(" ^^^^^ Deploying your app... ^^^^^")

    if not os.path.exists(CONFIG_FILE):
        click.echo("..... Config not found. Run `init` first.")
        return

    with open(CONFIG_FILE) as f:
        metadata = json.load(f)

    stack = metadata["stack"]
    app_path = metadata["app_path"]

    dockerfile_path = write_dockerfile(stack, app_path)
    click.echo(" ***** Dockerfile created successfully.")

    # DockerHub credentials & image tag
    username = "abhishekn12"
    repo = "myrepo"
    token = "dckr_pat_bHMZ49KpMA1gwf50WQZ_vNrPy3s"
    key_path = "c:/Users/Minfy/Desktop/cli_tool/terraform/my-key.pem"
    provision_infrastructure()

    timestamp = int(time.time())
    tag = f"{username}/{repo}:{timestamp}"

    ec2_ip = deploy_to_ec2(tag, username, repo, token, key_path, app_path)

    metadata["ec2_ip"] = ec2_ip
    with open(CONFIG_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

    # Ensure deployment folder exists
    os.makedirs(".vercel", exist_ok=True)

    # Read or create deployment history
    deployments = []
    if os.path.exists(DEPLOYMENTS_FILE):
        try:
            with open(DEPLOYMENTS_FILE, "r") as f:
                deployments = json.load(f)
        except json.JSONDecodeError:
            deployments = []

    # Optional: Remove previous entry (keep only last N)
    if len(deployments) > 1:
        deployments.pop(0)

    deployments.append({"timestamp": timestamp, "tag": tag})

    with open(DEPLOYMENTS_FILE, "w") as f:
        json.dump(deployments, f, indent=2)

    click.echo(f"...... Deployment logged. Tag: {tag}")

@cli.command()
def monitor():
    click.echo(" ====== Setting up monitoring...")

    if not os.path.exists(CONFIG_FILE):
        click.echo("<><> Config not found. Run `init` first.")
        return

    key_path = "c:/Users/Minfy/Desktop/cli_tool/terraform/my-key.pem"

    with open(CONFIG_FILE) as f:
        metadata = json.load(f)

    ec2_ip = metadata.get("ec2_ip")
    if not ec2_ip:
        click.echo("...... EC2 IP not found. Run `deploy` first.")
        return

    monitoring_set(key_path, ec2_ip)
    click.echo("##### Monitoring configured.")

@cli.command()
def rollback():
    rollback_cmd()

@cli.command()
def destroy():
    destroy_ec2()

if __name__ == "__main__":
    cli()
