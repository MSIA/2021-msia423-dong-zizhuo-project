# MSiA423 Project

Author: Zizhuo (Xavier) Dong

QA: Wenyang Pan

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


## Deployed app URL:

http://searc-Publi-AS77N2FV3OSM-1020167833.us-east-2.elb.amazonaws.com

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



#### Please note: Python version 3.6> required

## Instruction to run data pipeline

#### Set AWS access key

- Set your environment variables for AWS in terminal:
  * `export AWS_ACCESS_KEY_ID='<your aws-access-key-id>'`\
  `export AWS_SECRET_ACCESS_KEY=<your aws-secret-access-key>` 

#### Set mysql connection variable
- Set your environment variables for mysql in terminal:
  * `export MYSQL_USER=<your_username>` \
  `export MYSQL_PASSWORD=<your_password>` \
  `export MYSQL_HOST=<your_rds_endpoint>` \
  `export MYSQL_PORT=<your_rds_port>` \
  `export DATABASE_NAME=<your_database_name>`
  
#### Edit config.py

- Open `config/config.py`
  * edit `LOCAL_DATA_PATH` to the path where you want the raw data to be downloaded locally 
  * edit `S3_DATA_PATH` to the path where you want to upload the raw data in s3


### Build Docker Image

- Connect to Northwestern VPN
- In terminal, change directory to root directory of project `<local_path>/2021-msia423-dong-zizhuo-project/` 
- Run the following command in terminal

    `docker build -f app/Dockerfile -t searchfrisk .` 
  
### Ingesting data 

#### Upload to S3

```
python run.py ingest --local_path {your_local_data_path} --s3_path {your_s3_data_path}
```

#### Upload to S3 with docker
```
docker run -it \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    searchfrisk run.py ingest --local_path {your_local_data_path} --s3_path {your_s3_data_path}
```

`--local_path` and `--s3_path` argument are optional if you set a default value for `LOCAL_DATA_PATH` and `S3_DATA_PATH` in `config.py`

### Create the database

- By default, `python run.py create_db` creates a mysql database at `sqlite:///data/msia423_db.db` if `MYSQL_HOST` is not defined as an environment variable
- if `MYSQL_HOST` environment variable defined, a mysql database will be created in RDS

#### Creating local mysql database in sqlite

```
python run.py create_db --engine_string {your_local_engine_string}
```

#### Creating local mysql database in sqlite (using docker)

```
docker run searchfrisk run.py create_db --engine_string {your_local_engine_string}
```

#### Creating mysql database in RDS 

```
python run.py create_db --engine_string {your_rds_engine_string}
```
#### Creating mysql database in RDS (using docker) 

```
docker run -it 
    -e MYSQL_HOST \ 
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    searchfrisk run.py create_db --engine_string {your_rds_engine_string}'
```

### Connect to database using docker

Run the following docker command in terminal to connect to mysql database in RDS

```
docker run -it --rm \
    mysql:5.7.33 \
    mysql \
    -h${MYSQL_HOST} \
    -u${MYSQL_USER} \
    -p${MYSQL_PASSWORD}
```

After making a connection to your RDS mysql database

```
show databases;
use <your_database_name>
show tables;
```
Verify that table `ModelResult` has been successfully created in your RDS database

### Running the model

#### Train model and save model and result

```
python run.py run_model --input {your_local_data_path} --config {your_model_config_path}
```

#### Train model and save model and result with docker

```
docker run searchfrisk run.py run_model --input {your_local_data_path} --config {your_model_config_path}
```

### Ingesting result 

#### Upload model result to S3

```
python run.py ingest_result --local_path {your_local_result_path} --s3_path {your_s3_result_path}
```

#### Upload model result to S3 with docker
```
docker run -it \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    searchfrisk run.py ingest_result --local_path {your_local_result_path} --s3_path {your_s3_result_path}
```

`--local_path` and `--s3_path` argument are optional if you set a default value for `LOCAL_RESULT_PATH` and `S3_RESULT_PATH` in `config.py`

### Add result to database 

#### Upload model result as a table to RDS

```
python run.py add_result --input {your_result_path(local or s3)} --engine_string {your_rds_engine_string}
```

#### Upload model result as a table to RDS with docker

```
docker run -it 
    -e MYSQL_HOST \ 
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    searchfrisk run.py add_result --input {your_result_path(local or s3)} --engine_string {your_rds_engine_string}
```


## Running the app

### Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/sqf-15.db'  # URI (engine string) for database that contains tracks
APP_NAME = "searchfrisk"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at `http://localhost:5000/` in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
docker build -f app/Dockerfile -t searchfrisk .
```

This command builds the Docker image, with the tag `searchfrisk`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -it -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e DATABASE_NAME -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -p 5000:5000 --name test searchfrisk
```
You should now be able to access the app at `http://localhost:5000/` in your browser.

This command runs the `searchfrisk` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port.

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.


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
 
