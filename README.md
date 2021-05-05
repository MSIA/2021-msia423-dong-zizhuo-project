# MSiA423 Project

Author: Zizhuo (Xavier) Dong

QA: Wenyang Pan

## Instruction to run data pipeline
- Set your environment variables for AWS in terminal:
  * `export AWS_ACCESS_KEY_ID='<your aws-access-key-id>'`  
  * `export AWS_SECRET_ACCESS_KEY=<your aws-secret-access-key>`  
  * `export BUCKET_NAME=msia423-dong`  

- Open `src/config.py` and edit `local_data_path` to the path where you want the raw data to be downloaded locally and `s3_data_path` to the path where you want to upload the raw data in s3
 
- Execute docker command file `run_load_data.sh` and `run_generate_db.sh` to run data pipeline

## Project Charter 

#### Background 

In the US, police brutality and systemic racism is a very serious social issue.

I believe this issue can potentially benefit from further research to discover more insights through a data-driven modeling approach on historical data collected in practical real-world scenarios.

#### Vision

The New York City Stop and Frisk Program allows officers with NYPD to Stop, Question, Frisk, and Search civilians in public. This program has garnished a significant amount of attention due to its questionable constitutionality and effectiveness. Statistical studies indicate an imbalance on who the Stop and Frisk Program was applied to most. Moreover, there is little to no evidence that the program was effective at all in deterring crime. 

The goal of the project is to utilize historical data on NYC's search and frisk program to build a tool that can accurately classify someone's likelihood of being searched or frisked.

This could be useful to many people such as:
* Lawyer/Policy Maker (criminal defense and justice system reform)
* Police Officer (resource/budget distribution)
* Social Activist (policy change, sociology application)
* Regular Citizens (when and where to avoid, and chances of confronted by police)
* Criminals? (How to avoid the police confrontation after committing a crime)

#### Mission
Because of the issues mentioned above, we would like to build a classifier app that can predict whether or not a person will be frisked/searched given certain features of that person.
In this app, the user will have the option to input features such as the ones list below:

* age, sex, height, race
* location
* time of day
* crime suspected
* drug/weapon involved
* physical force

The output will be the probability of being searched or frisked given the features that the user input, it will also provide visualization to show the most influencing features that model used to determine the probabilities.

The datasets I chose are from the public NYPD stop and frisk report website and contain details and statistics for New York City Police Department’s Stop, Question and Frisk program for 2003-2016. Features include the time, date of stop, offense, suspect description, the reason for stop/arrest, whether there were a weapon, contraband and other additional circumstances related to the stop. In total, we have around 3.4 million records with 115 features in the raw data.
While this is a large dataset, the dataset is very sparse (a lot of missing features), so a lot of records will be excluded after data preprocessing and feature selection. Aggregations of certain group hierarchy within the will also be performed to reduce the size of the dataset.

#### Success Criteria

#### Machine Learning Metrics

Since the dataset is labeled, it is suitable for supervised learning machine learning methods, the following models are scheduled to be fitted:
* Random Forest Classifier
* Logistic Regression
* Naive Bayes Classifier
* XGBoost

The metric that will be used to evaluate the classifier include: mis-classification rate/accuracy, precision/recall, and the ROC curve. These metrics will give us an indication of the predictive power of the underlying model built at predicting whether a suspect will be frisked or searched. The model will use all of the data except for the last year (2013) to train and test on the 2013 dataset. A classification accuracy of 70% at predicting search and frisked is a reasonable goal since the majority class (not searched/frisked) is about 60% of the data, this goal will beat guessing the majority by a good margin.
Performance metrics such as the model's run time and computational resources required to train the model, as well as scalability (for example if deployed in a brand new city) should also be considered.

#### Business Metrics

From a business perspective, a successful deployment of this tool can expose any underlying bias in the current policing system and provide evidence to set the stage for progressive social movement/changes, as well as guiding policy changes in the police system.
We can potentially quantify the effectiveness of the app in this aspect by collecting data on the demographics of users and how the app suits their intended purposes 
Their frequency of use and feedbacks on how they use the app to help them do their job can be consulted for whether the app is successful from a business perspective


<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database 
To create the database in the location configured in `config.py` run: 

`python run.py create_db --engine_string=<engine_string>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db`.

#### Adding songs 
To add songs to the database:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.

### Example using `python3` as an entry point

We have included another example of a Dockerfile, `app/Dockerfile_python` that has `python3` as the entry point such that when you run the image as a container, the command `python3` is run, followed by the arguments given in the `docker run` command after the image name. 

To build this image: 

```bash
 docker build -f app/Dockerfile_python -t pennylane .
```

then run the `docker run` command: 

```bash
docker run -p 5000:5000 --name test pennylane app.py
```

The new image defines the entry point command as `python3`. Building the sample PennyLane image this way will require initializing the database prior to building the image so that it is copied over, rather than created when the container is run. Therefore, please **do the step [Create the database with a single song](#create-the-database-with-a-single-song) above before building the image**.

# Testing

From within the Docker container, the following command should work to run unit tests when run from the root of the repository: 

```bash
python -m pytest
``` 

Using Docker, run the following, if the image has not been built yet:

```bash
 docker build -f app/Dockerfile_python -t pennylane .
```

To run the tests, run: 

```bash
 docker run penny -m pytest
```
 