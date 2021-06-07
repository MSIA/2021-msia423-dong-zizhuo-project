import traceback
import logging.config
from flask import Flask
from flask import render_template, request

from src.generate_db import ModelResult, ModelResultManager

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session

model_result_manager = ModelResultManager(app)

logger.info('Database used: %s', app.config['SQLALCHEMY_DATABASE_URI'].split(':')[0])


@app.route('/')
def index():
    """Main view.

    Create view into index page that uses data queried from ModelResult database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        results = model_result_manager.session.query(ModelResult).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', results=results)
    except:
        traceback.print_exc()
        logger.warning("Not able to display result, error page returned")
        return render_template('error.html')


@app.route('/', methods=['POST'])
def data():
    """View that process a POST with new result input

    :return: redirect to index page
    """

    if request.method == 'POST':
        user_input_sex = request.form.to_dict()['sex']
        user_input_race = request.form.to_dict()['race']
        user_input_age = request.form.to_dict()['age']

        try:
            results = model_result_manager.session.query(ModelResult).filter_by(
                sex=user_input_sex,
                race=user_input_race,
                age=user_input_age,
            ).limit(app.config["MAX_ROWS_SHOW"]).all()
            return render_template('index.html', results=results)
        except:
            traceback.print_exc()
            logger.warning("Not able to display tracks, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
