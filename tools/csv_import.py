import csv
from flask import current_app
from config import ConfigKeys


def get_csv_data():
    with open(current_app.config.get(ConfigKeys.APP_CSV_PATH.value), newline='') as csvfile:
        return list(csv.reader(csvfile, delimiter=';', quotechar='|'))
