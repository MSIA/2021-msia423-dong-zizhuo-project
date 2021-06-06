import argparse
import logging.config

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger(__name__)

import src.model as model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    sb_model = subparsers.add_parser("train_model", description="train model")
    sb_model.add_argument("--input", '-i', default=None, help="path to input data")
    sb_model.add_argument("--config", default=None, help="path to model config file")
    sb_model.set_defaults(func=model.run)

    # Parse args and run corresponding pipeline
    args = parser.parse_args()
    args.func(args)



    '''
    
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
