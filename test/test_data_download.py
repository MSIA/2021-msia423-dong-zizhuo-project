import boto3
import pandas as pd

s3 = boto3.resource("s3")
bucket = s3.Bucket("msia423-dong")
# bucket.upload_file("file-name-to-upload", "/s3-path/to/nypd_sf")

df = pd.read_csv('s3://msia423-dong/nypd_sf/NYPD_SF_2003.csv', low_memory=False)
print(df.shape)
