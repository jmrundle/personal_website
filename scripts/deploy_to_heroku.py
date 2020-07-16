#!/usr/bin/env python3

from config.app_config import BaseConfig
import boto3
from scripts import setup_heroku, setup_spotify

BUCKET_NAME  = BaseConfig.S3_BUCKET
REGION       = BaseConfig.AWS_DEFAULT_REGION
RESOURCE_DIR = BaseConfig.RESOURCE_DIR
CACHE_PATH   = BaseConfig.SPOTIFY_CACHE_PATH


def bucket_exists(bucket_name):
    s3 = boto3.resource('s3')
    return s3.Bucket(bucket_name).creation_date is not None


# authorize scopes and generate token file
setup_spotify.main()


# upload token file to S3
client = boto3.client('s3')

if not bucket_exists(BUCKET_NAME):
    client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={"LocationConstraint": REGION })

client.upload_file(CACHE_PATH, BUCKET_NAME, ".spotify-cache")
"""
# push all resources to S3 (so we don't have to store in GIT)
for filename in os.listdir(RESOURCE_DIR):
    if filename.startswith("."):
        continue

    rel_path = os.path.relpath(filename, __file__)
    s3.upload_file(rel_path, BUCKET_NAME, filename)
"""

# set heroku config vars from .env
setup_heroku.main()
