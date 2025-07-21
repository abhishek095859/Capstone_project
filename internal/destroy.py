import os
import json
import click
import subprocess

CONFIG_PATH = ".vercelcli.json"
TERRAFORM_DIR = "terraform"

def destroy_ec2():
    click.echo(" ## --- ## Destroying EC2 infrastructure...")

    if not os.path.exists(CONFIG_PATH):
        click.echo(" No config found. Did you run init/deploy?")
        return

    # Step 1: Run `terraform destroy`
    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=TERRAFORM_DIR, check=True)
        click.echo(" ------  EC2 instance destroyed.")
    except subprocess.CalledProcessError:
        click.echo(" ==== /// ==== Terraform destroy failed.")
        return

    # Step 2: Delete local config files