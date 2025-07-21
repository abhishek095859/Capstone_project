import os
import boto3

def upload_folder_to_s3(repo_path, bucket_name="mini-vercel", s3_prefix="" , profile_name="my-sso"):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, repo_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            #print(f"======== Uploading {local_path} to s3://{bucket_name}/{s3_key}")
            s3.upload_file(local_path, bucket_name, s3_key)

    print("+++++++ Upload complete.")


