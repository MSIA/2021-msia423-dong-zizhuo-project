import os
from os import path
import logging

# project home path
project_home_path = path.dirname(path.abspath(__file__))

# logging config
logging_config = path.join(project_home_path, '../config/logging/local.conf')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# data source
data_url = "https://www1.nyc.gov/assets/nypd/downloads/excel/analysis_and_planning/stop-question-frisk/sqf-2015.csv"

# local data path
local_data_path = "C:/Users/dongz/PycharmProjects/2021-msia423-dong-zizhuo-project/data/raw/sqf-2015.csv"

# s3 data path
s3_data_path = "s3://msia423-dong/raw/sqf-2015.csv"

# RDS MYSQL Credentials
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
db_name = os.environ.get("DATABASE_NAME")
engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"

