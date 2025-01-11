"""
In this script, I aim to verify whether my Python package was created as intended.

In the field of Data Analytics, one of the most widely used Python packages is pandas—arguably the most essential.
I've always been impressed by how user-friendly this package is.

I believe its intuitive API design and consistent naming conventions are key factors behind the library's success
and effectiveness.
"""
import os

import pandas as pd
import yaqtools as yaqt

from datetime import datetime, timedelta

import logging
logging.basicConfig(level=logging.INFO)

def get_datetime_list(dt, periods=100):
    date_list = []
    for x in range(0, periods):
        date_list.append(dt - timedelta(days=x))
    return date_list

def get_timestamp_list(dt, periods):
    return  pd.date_range(dt, periods=periods).tolist()

def demo_df_types():

    dates = get_datetime_list(datetime.now(), periods=20)
    dates_pd = get_timestamp_list(datetime.now(), periods=20)
    ints = [i for i in range(0, 20)]
    df = pd.DataFrame(list(zip(dates, dates_pd, ints)), columns=["date_python", "date_pandas", "number"])

    assert type(yaqt.is_datetime(df["date_python"])) is bool

    if yaqt.is_datetime(df["date_python"]):
        logging.info("The col 'date_python' is a datetime")

    if yaqt.is_datetime(df["date_pandas"]):
        logging.info("The col 'date_pandas' is a datetime")

    if not yaqt.is_datetime(df["number"]):
        logging.info("The col 'number' is a not datetime")

    if yaqt.is_numeric(df["number"]):
        logging.info("The col 'number' is a numeric")

def demo_mapping():

    dates = get_datetime_list(datetime.now(), periods=20)
    ints = [i for i in range(0, 20)]
    df_origin = pd.DataFrame(list(zip(dates, ints)), columns=["date", "number"])

    df_destination = pd.DataFrame(dates, columns=["date"])
    df_destination["number"] = None

    logging.info(yaqt.is_numeric(df_destination["number"]))

    expected_schema = yaqt.map_df_schema(df_destination, df_origin)
    for value in expected_schema:
        logging.info(value)

def demo_dates():

    logging.info(yaqt.to_utc_datetime("2025-01-11", exp_fmt="%Y-%m-%d"))
    date_aware = yaqt.to_utc_datetime("2025-01-11 10:00:05", exp_fmt="%Y-%m-%d %H:%M:%S")
    logging.info(date_aware)
    assert type(date_aware) != type(datetime(2025, 1, 11).date())

def demo_io():
    lists = yaqt.get_list_files(os.getcwd(), ".py")
    logging.info(f"There are {len(lists)} files in the current directory")
    logging.info(f"The files names are {[os.path.basename(file) for file in lists]}")

if __name__ == "__main__":

    demo_df_types()
    demo_mapping()
    demo_dates()
    demo_io()





