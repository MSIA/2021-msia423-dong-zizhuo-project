import sys
import pandas as pd
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
import logging
import warnings
warnings.simplefilter("ignore")

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


def create_db(args):
    """
    create new table in AWS RDS

    Args:
        engine_string [string]: mysql connection engine string to create table at
    Returns:
        None
    """

    try:
        logger.debug("Attempting to create database")
        engine = sqlalchemy.create_engine(args.engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database generated")
    except sqlalchemy.exc.OperationalError:
        logger.error("Incorrect mysql credentials!")
        sys.exit(1)


class ModelResult(Base):
    """
    create new table in AWS RDS
    """

    __tablename__ = 'ModelResult'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pct = Column(Integer, unique=False, nullable=True)
    perobs = Column(Integer, unique=False, nullable=True)
    arstmade = Column(String(100), unique=False, nullable=True)
    offunif = Column(String(100), unique=False, nullable=True)
    sex = Column(String(100), unique=False, nullable=True)
    race = Column(String(100), unique=False, nullable=True)
    age = Column(Integer, unique=False, nullable=True)
    weight = Column(Integer, unique=False, nullable=True)
    height = Column(Integer, unique=False, nullable=True)
    predicted_searched = Column(String(100), unique=False, nullable=True)
    actual_searched = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return f'<id: {self.id}, predicted_searched {self.predicted_searched}, actual_searched {self.predicted_searched}'


class ModelResultManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app (Flask): Flask app
            engine_string (str): Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def add_result(self, input):
        """
        create result table in RDS

        Args:
            input [string]: input path of result data
        Returns:
            None
        """

        session = self.session

        logger.info('Session initialized')

        persist_list = []
        data_list = pd.read_csv(input).to_dict(orient='records')

        for data in data_list:
            persist_list.append(ModelResult(**data))
        session.add_all(persist_list)

        session.commit()
        logger.info('%s records were added to the table', len(persist_list))

    def close(self):
        """
        Closes session

        Returns: None
        """
        self.session.close()

