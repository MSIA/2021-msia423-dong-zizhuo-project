import argparse
import logging
import logging.config as logging_conf
import src.load_data as load_data
import src.generate_db as gen_db
import src.model as model
import config.config as config
from src.generate_db import ModelResultManager
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

local_data_path = config.LOCAL_DATA_PATH
s3_data_path = config.S3_DATA_PATH
model_config_path = config.MODEL_CONFIG_PATH
local_result_path = config.LOCAL_RESULT_PATH
s3_result_path = config.S3_RESULT_PATH

logging_conf.fileConfig('config/logging/local.conf')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    # Sub-parser for uploading data to S3 bucket
    sb_upload = subparsers.add_parser("ingest", description="upload data to S3 buckets")
    sb_upload.add_argument('--local_path', required=False, help='local path of raw data', default=local_data_path)
    sb_upload.add_argument('--s3_path', required=False, help='path to store raw data on S3', default=s3_data_path)
    sb_upload.set_defaults(func=load_data.upload_data_to_s3)

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="create database")
    sb_create.add_argument("--engine_string", required=False, help="mysql connection engine string",
                           default=SQLALCHEMY_DATABASE_URI)
    sb_create.set_defaults(func=gen_db.create_db)

    # Sub-parser for training model
    sb_model = subparsers.add_parser("run_model", description="run model")
    sb_model.add_argument("--input", '-i', required=False, default=local_data_path, help="path to input raw data")
    sb_model.add_argument("--config", required=False, default=model_config_path, help="path to model config file")
    sb_model.set_defaults(func=model.run_model)

    # Sub-parser for uploading result to S3 bucket
    sb_upload = subparsers.add_parser("ingest_result", description="upload data to S3 buckets")
    sb_upload.add_argument('--local_path', required=False, help='local path of raw data', default=local_result_path)
    sb_upload.add_argument('--s3_path', required=False, help='path to store raw data on S3', default=s3_result_path)
    sb_upload.set_defaults(func=load_data.upload_result_to_s3)

    # Sub-parser for ingesting result into rds database
    sb_model = subparsers.add_parser("add_result", description="add model result to database")
    sb_model.add_argument("--input", '-i', required=False, default=local_result_path, help="path to model result data")
    sb_model.add_argument("--engine_string", required=False, help="mysql connection engine string",
                          default=SQLALCHEMY_DATABASE_URI)

    # Parse args and run corresponding pipeline
    args = parser.parse_args()

    sp_used = args.subparser
    if sp_used == 'ingest':
        load_data.upload_data_to_s3(args)
    elif sp_used == 'create_db':
        gen_db.create_db(args)
    elif sp_used == 'run_model':
        model.run_model(args)
    elif sp_used == 'ingest_result':
        load_data.upload_result_to_s3(args)
    elif sp_used == 'add_result':
        mrm = ModelResultManager(engine_string=args.engine_string)
        mrm.add_result(args.input)
        mrm.close()
    else:
        parser.print_help()

