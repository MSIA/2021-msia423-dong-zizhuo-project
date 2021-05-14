import argparse
import logging.config

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger(__name__)

import src.load_data as load_data
import src.generate_db as gen_db
import config.config as config
local_data_path = config.LOCAL_DATA_PATH
s3_data_path = config.S3_DATA_PATH

from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Sub-parser for uploading data to S3 bucket
    sb_upload = subparsers.add_parser("ingest", description="upload data to S3 buckets")
    sb_upload.add_argument('--local_path', required=False, help='local path of raw data', default=local_data_path)
    sb_upload.add_argument('--s3_path', required=False, help='path to store raw data on S3', default=s3_data_path)
    sb_upload.set_defaults(func=load_data.upload_file_to_s3)

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="create database")
    sb_create.add_argument("--engine_string", required=False, help="mysql connection engine string",
                           default=SQLALCHEMY_DATABASE_URI)
    # sb_create.add_argument("--local", required=False, help="local database or not",
    #                        default=True)
    sb_create.set_defaults(func=gen_db.create_db)

    # Parse args and run corresponding pipeline
    args = parser.parse_args()
    args.func(args)

    '''
    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")
    
    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--artist", default="Emancipator", help="Artist of song to be added")
    sb_ingest.add_argument("--title", default="Minor Cause", help="Title of song to be added")
    sb_ingest.add_argument("--album", default="Dusk to Dawn", help="Album of song being added")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/tracks.db',
                           help="SQLAlchemy connection URI for database")
    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        tm = TrackManager(engine_string=args.engine_string)
        tm.add_track(args.title, args.artist, args.album)
        tm.close()
    else:
        parser.print_help()
    '''
