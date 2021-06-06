from src.load_data import parse_s3
import warnings
warnings.simplefilter("ignore")


def test_parse_s3():
    s3_path = "s3://msia423-dong/raw/sqf-2015.csv"
    s3bucket, s3path = parse_s3(s3_path)
    expected_bucket = "msia423-dong"
    expected_path = "raw/sqf-2015.csv"
    assert s3bucket == expected_bucket and s3path == expected_path


def test_parse_s3_unhappy():
    s3_path = "./data/raw/sqf-2015.csv"
    try:
        s3bucket, s3path = parse_s3(s3_path)
    except:
        assert True

