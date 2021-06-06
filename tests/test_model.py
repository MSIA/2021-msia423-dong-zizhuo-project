import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")

from src.model import clean_data, preprocess_data


def test_clean_data():
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    input_df = input_df.head(1000)
    output_df = clean_data(input_df)
    check_null = output_df.isnull().values.any()
    assert check_null != True


def test_clean_data_unhappy():
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    test_df = pd.DataFrame([],
                           columns=list(input_df.columns.values))
    output_df = clean_data(test_df)
    num_row = np.shape(output_df)[0]
    assert num_row == 0


def test_preprocess_data():
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    input_df = clean_data(input_df)
    feature_df, label_df, raw_f_test = preprocess_data(input_df)
    test_cols = ['pct', 'arstmade', 'offunif', 'sex', 'race', 'searched']
    df_cols = list(feature_df.columns.values)
    result = False
    for x in df_cols:
        for y in test_cols:
            if x == y:
                result = True
    assert result != True


def test_preprocess_data_unhappy():
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    input_df = clean_data(input_df)
    feature_df, label_df, raw_f_test = preprocess_data(input_df)
    test_cols = ['perobs', 'age', 'weight', 'height']
    df_cols = list(feature_df.columns.values)
    result = set(test_cols).issubset(df_cols)
    assert result == True




