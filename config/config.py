import os
from os import path

# project home path
PROJECT_HOME = path.dirname(path.abspath(__file__))

# logging config
LOGGING_CONFIG = path.join(PROJECT_HOME, 'logging/local.conf')

# data source
DATA_URL = "https://www1.nyc.gov/assets/nypd/downloads/excel/analysis_and_planning/stop-question-frisk/sqf-2015.csv"

# local data path
LOCAL_DATA_PATH = "./data/raw/sqf-2015.csv"

# s3 data path
S3_DATA_PATH = "s3://msia423-dong/raw/sqf-2015.csv"

# model config file path
MODEL_CONFIG_PATH = "./config/model_config.yml"

# local result path
LOCAL_RESULT_PATH = "./data/result.csv"

# s3 result path
S3_RESULT_PATH = "s3://msia423-dong/result.csv"

# RDS MYSQL Credentials
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
db_name = os.environ.get("DATABASE_NAME")
ENGINE_STRING = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"

