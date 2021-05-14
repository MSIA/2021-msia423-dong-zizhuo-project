import sys
import argparse
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float
import logging


logger = logging.getLogger(__name__)

Base = declarative_base()


class ModelResult(Base):
    """
    create new table in AWS RDS
    """

    __tablename__ = 'ModelResult'

    model_name = Column(String(100), primary_key=True, nullable=False)
    accuracy = Column(Float, unique=False, nullable=True)
    precision = Column(Float, unique=False, nullable=True)
    recall = Column(Float, unique=False, nullable=True)
    roc_auc = Column(Float, unique=False, nullable=True)

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
