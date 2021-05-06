import os
import argparse
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
# from sqlalchemy.orm import sessionmaker
import sqlalchemy
import logging

Base = declarative_base()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

conn_type = "mysql+pymysql"
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("DATABASE_NAME")
ENGINE_STRING = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"


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


def generate_new_db(args):
    """
    create new table in AWS RDS

    Args:
        engine_string [string]: mysql connection engine string to create table at
    Returns:
        None
    """
    try:
        engine = sqlalchemy.create_engine(args.engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database generated")
    except sqlalchemy.exc.OperationalError:
        logger.error("Incorrect mysql credentials!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pass in engine string to generate new database.")
    parser.add_argument("--engine_string", default=ENGINE_STRING,
                        help="mysql engine string")
    arg = parser.parse_args()

    generate_new_db(ENGINE_STRING)
