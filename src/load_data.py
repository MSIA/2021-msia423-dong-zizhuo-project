import boto3
import botocore
import sys
import os
from io import StringIO
import pandas as pd
import requests
import logging
import argparse
import yaml
import re
import src.config as config
data_url = config.data_url
local_data_path = config.local_data_path
s3_data_path = config.s3_data_path

logger = logging.getLogger(__name__)


def download_data(local_path=local_data_path):
    """
    download static, public, data file into python using the request library, and convert to pandas dataframe

    Args:
        local_path: local path to download raw data to
    Returns:
        data: raw data as a pandas dataframe
    """

    try:
        r = requests.get(data_url)
    except requests.exceptions.RequestException:
        logger.error("Unable to download raw data from data source")
        sys.exit(1)

    text = r.text
    textIO = StringIO(text)
    data = pd.read_csv(textIO, sep=',')
    data.to_csv(local_path, sep=',', index=False)
    return data


def parse_s3(s3path):
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(args):
    download_data(args.local_path)

    s3bucket, s3_just_path = parse_s3(args.s3_path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)
    try:
        bucket.upload_file(args.local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', args.local_path, args.s3_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--s3_path', default=s3_data_path,
                        help="Where to upload data into S3")
    parser.add_argument('--local_path', default=local_data_path,
                        help="Where to find raw data to be uploaded locally")
    args = parser.parse_args()

    upload_file_to_s3(local_data_path, s3_data_path)
