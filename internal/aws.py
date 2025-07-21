# internal/aws/setup_infra.py

import subprocess

def provision_infrastructure():
    """Run Terraform to provision EC2 + S3"""
    try:
        subprocess.run(["terraform", "init"], check=True, cwd="terraform/")
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True, cwd="terraform/")
        subprocess.run([
    "terraform", "output", "-json"
], cwd="terraform", stdout=open("terraform/output.json", "w"))
    except subprocess.CalledProcessError:
        print("******* Terraform provisioning failed.")

