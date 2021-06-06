import boto3
import botocore
import sys
from io import StringIO
import pandas as pd
import requests
import logging
import re
import config.config as config

data_url = config.DATA_URL
local_data_path = config.LOCAL_DATA_PATH
s3_data_path = config.S3_DATA_PATH

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def download_data(local_path=local_data_path):
    """
    download static, public, data file into python using the request library, save csv to local path, and convert to pandas dataframe

    Args:
        local_path [string]: local path to download raw data to
    Returns:
        data [pandas dataframe]: raw data as a pandas dataframe
    """

    try:
        logger.debug("Attempting to download raw data from data source")
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
    """
    parse s3path into bucket name and path

    Args:
        s3path [string]: s3 path to upload raw data
    Returns:
        s3bucket [string]: bucket name to upload raw data to
        s3path [string]: path in s3bucket to upload raw data to
    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(args):
    """
    upload raw data files to s3 bucket

    Args:
        local_path [string]: local path to download raw data
        s3_path [string]: s3 path to upload raw data
    Returns:
        None
    """
    download_data(args.local_path)

    s3bucket, s3_just_path = parse_s3(args.s3_path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)
    try:
        logger.debug("Attempting to upload raw data to s3")
        bucket.upload_file(args.local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', args.local_path, args.s3_path)


def upload_result_to_s3(args):
    """
    upload result files to s3 bucket

    Args:
        local_path [string]: local path to result data
        s3_path [string]: s3 path to upload result data
    Returns:
        None
    """

    s3bucket, s3_just_path = parse_s3(args.s3_path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)
    try:
        logger.debug("Attempting to upload raw data to s3")
        bucket.upload_file(args.local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', args.local_path, args.s3_path)
