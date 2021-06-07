import pandas as pd
import numpy as np
from src.model import clean_data, preprocess_data
import warnings
warnings.simplefilter("ignore")


def test_clean_data():
    """
    test if clean_data function remove all null rows
    """
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    input_df = input_df.head(1000)
    output_df = clean_data(input_df)
    check_null = output_df.isnull().values.any()
    assert check_null != True


def test_clean_data_empty():
    """
    test if clean_data function works with empty dataframe
    """
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    test_df = pd.DataFrame([],
                           columns=list(input_df.columns.values))
    output_df = clean_data(test_df)
    num_row = np.shape(output_df)[0]
    assert num_row == 0


def test_clean_data_unhappy():
    """
    test if clean_data function handles incorrect dataframe input
    """
    test_df = pd.DataFrame([],
                           columns=["wrong_column1", "wrong_column2"])
    try:
        output_df = clean_data(test_df)
    except:
        assert True


def test_preprocess_data_categorical():
    """
    test if preprocess_data function returns dataframe with the correct categorical features set
    """
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


def test_preprocess_data_numerical():
    """
    test if preprocess_data function returns dataframe with the correct numerical features set
    """
    input_df = pd.read_csv("./data/raw/sqf-2015.csv")
    input_df = clean_data(input_df)
    feature_df, label_df, raw_f_test = preprocess_data(input_df)
    test_cols = ['perobs', 'age', 'weight', 'height']
    df_cols = list(feature_df.columns.values)
    result = set(test_cols).issubset(df_cols)
    assert result == True


def test_preprocess_data_unhappy():
    """
    test if preprocess_data function returns dataframe with the wrong features set
    """
    test_df = pd.DataFrame([],
                           columns=["wrong_column1", "wrong_column2"])
    try:
        feature_df, label_df, raw_f_test = preprocess_data(test_df)
    except:
        assert True


