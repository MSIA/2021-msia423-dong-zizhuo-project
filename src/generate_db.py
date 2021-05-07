import sys
import argparse
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import logging
import config.config as config

ENGINE_STRING = config.ENGINE_STRING

logger = logging.getLogger(__name__)

Base = declarative_base()


class ModelResult(Base):
    """
    create new table in AWS RDS
    """

    __tablename__ = 'ModelResult'

    model_name = Column(String(100), primary_key=True, nullable=False)
    accuracy = Column(Integer, unique=False, nullable=True)
    precision = Column(Integer, unique=False, nullable=True)
    recall = Column(Integer, unique=False, nullable=True)
    roc_auc = Column(Integer, unique=False, nullable=True)

    def __repr__(self):
        return f'<ModelResult model {self.model_name} accuracy {self.accuracy} precision {self.precision} recall {self.recall} roc_auc {self.roc_auc} '


def create_db(args):
    """
    create new table in AWS RDS

    Args:
        engine_string [string]: mysql connection engine string to create table at
        local [boolean]: whether to create local database or in RDS
    Returns:
        None
    """

    try:
        engine = sqlalchemy.create_engine(args.engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database generated:")
        logger.info(args.engine_string)
    except sqlalchemy.exc.OperationalError:
        logger.error("Incorrect mysql credentials!")
        sys.exit(1)

    # Show all tables with log
    # if not args.local:
    #     query = "show tables;"
    #     df = pd.read_sql(query, con=engine)
    #     logger.info('Tables: {}'.format(list(df.iloc[:, 0])))
    # else:
    #     pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pass in engine string to generate new database.")
    parser.add_argument("--engine_string", default=ENGINE_STRING,
                        help="mysql engine string")
    parser.set_defaults(func=create_db)
    args = parser.parse_args()
    args.func(args)

    # create_db(ENGINE_STRING)
