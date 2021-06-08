import logging
import yaml
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.simplefilter("ignore")
from src.load_data import download_data_from_s3

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_data(dataframe):
    """
    clean raw data

    Args:
        dataframe [pandas dataframe]: raw data as a pandas dataframe
    Returns:
        dataframe_rel [pandas dataframe]: cleaned data as a pandas dataframe
    """

    # combine ht_feet and ht_inch to convert height in inches
    dataframe['height'] = 12 * dataframe['ht_feet'] + dataframe['ht_inch']
    dataframe.drop(['ht_feet', 'ht_inch'], axis=1, inplace=True)

    # get hour of timestop
    dataframe['timestop'] = dataframe['timestop'].astype(str)
    dataframe['timestop_len'] = dataframe['timestop'].apply(lambda x: len(x))
    dataframe = dataframe[dataframe['timestop_len'] >= 3]
    dataframe['timestop_hour'] = dataframe['timestop'].apply(lambda x: x[0] if len(x) == 3 else x[0:2])

    # convert categorical variable to string
    dataframe['perobs'] = dataframe['perobs'].astype(int)
    dataframe['pct'] = dataframe['pct'].astype(str)

    # select only relevant columns needed for model
    rel_cols = ['pct', 'perobs', 'arstmade', 'offunif',
                'searched',
                'sex', 'race', 'age', 'weight', 'height']

    dataframe_rel = dataframe[rel_cols]

    # drop rows with bad data entry
    dataframe_rel.dropna(how='any', inplace=True)
    dataframe_rel.drop(dataframe_rel[dataframe_rel['pct'] == 999].index, inplace=True)
    dataframe_rel.drop(dataframe_rel[dataframe_rel['age'] == 999].index, inplace=True)
    dataframe_rel.drop(dataframe_rel[dataframe_rel['weight'] == 999].index, inplace=True)
    dataframe_rel.drop(dataframe_rel[dataframe_rel['height'] == 999].index, inplace=True)

    logger.info("Raw data cleaned.")

    return dataframe_rel


def preprocess_data(df, label="searched"):
    """
    prepare cleaned data for model training

    Args:
        df [pandas dataframe]: cleaned data as a pandas dataframe
        label [str]: label to be classified (searched)
    Returns:
        feature_df, label_df [pandas dataframes]: preprocessed dataframes for model training as a pandas dataframe
        raw_f_test [pandas dataframes]: original feature from tests set before preprocessing
    """
    label_df = df[label]
    raw_feature_df = df.drop(['searched'], axis=1)

    raw_f_train, raw_f_test, l_train, l_test = train_test_split(raw_feature_df, label_df, test_size=0.2, random_state=123)

    # scale numerical features with StandardScaler
    num_cols = ['perobs', 'age', 'weight', 'height']
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(raw_feature_df[num_cols])

    # One hot encode categorical variables
    cat_cols = ['pct', 'arstmade', 'offunif', 'sex', 'race']
    df = pd.concat([df, pd.get_dummies(df[cat_cols], prefix=cat_cols)], axis=1)
    df.drop(cat_cols, axis=1, inplace=True)

    feature_df = df.drop(['searched'], axis=1)

    logger.info("Feature dataframe and label dataframe created")

    return feature_df, label_df, raw_f_test


def train_model(feature_df, label_df, max_depth=14, max_features='sqrt', min_samples_leaf=1, output_model_path="./models/random_forest.sav"):
    """
    train and save classifier model

    Args:
        feature_df, label_df [pandas dataframes]: preprocessed dataframes for model training as a pandas dataframe
        saved_model_path [str]: path to saved trained model
    Returns:
        f_test, l_test [pandas dataframes]: tests set for making prediction
    """
    f_train, f_test, l_train, l_test = train_test_split(feature_df, label_df, test_size=0.2, random_state=123)
    forest_clf = RandomForestClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, max_features=max_features)
    forest_fit = forest_clf.fit(f_train, l_train)

    logger.info("Classifier model trained")

    joblib.dump(forest_fit, output_model_path)

    logger.info("Classifier model saved to %s" % output_model_path)
    return f_test, l_test


def predict(f_test, l_test, raw_f_test, saved_model_path, result_output_path):
    """
    predict probability of being searched of a new record

    Args:
        f_test [pandas dataframes]: feature tests set for making prediction
        l_test [pandas dataframes]: label tests set for making prediction
        raw_f_test [pandas dataframe]: original feature from tests set before preprocessing
        saved_model_path [str]: path to saved trained model
        result_output_path: path to save result dataframe as csv
    Returns:
        predicted_class [numpy array]: array of predicted binary value (yes or no to searched)
    """

    forest_fit = joblib.load(saved_model_path)
    predict_prob = np.rint(forest_fit.predict_proba(f_test))

    # get predicted probability of yes class of search
    predict_class = predict_prob[:, 1]

    # select only relevant columns needed result
    rel_cols = ['pct', 'perobs', 'arstmade', 'offunif',
                'sex', 'race', 'age', 'weight', 'height']

    raw_f_test = raw_f_test[rel_cols]
    raw_f_test["predicted_searched"] = pd.Series(data=predict_class)
    raw_f_test["predicted_searched"] = raw_f_test["predicted_searched"].map(lambda x: 'N' if x == 0 else 'Y')
    raw_f_test["actual_searched"] = l_test

    raw_f_test.to_csv(result_output_path, index=False)

    logger.info('The predicted result is saved to %s', result_output_path)

    return predict_class


def run_model(args):
    """
    Run the model training pipeline
    """

    logger.debug("Attempting to load model configuration file from %s" % args.config)

    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    download_data_from_s3(config['input']['local_data_path'], config['input']['s3_data_path'])
    raw_df = pd.read_csv(config['input']['local_data_path'])

    clean_df = clean_data(raw_df)
    feature_df, label_df, raw_f_test = preprocess_data(clean_df, config['preprocess']['label'])
    f_test, l_test = train_model(feature_df, label_df)

    logger.info("Attempting to make prediction on tests set")

    predict(f_test, l_test, raw_f_test, config['predict']['saved_model_path'], config['predict']['result_output_path'])

    logger.info("Prediction result saved to %s" % config['predict']['result_output_path'])
