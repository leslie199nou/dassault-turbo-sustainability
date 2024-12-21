import json
import os
from datetime import datetime
from flask import current_app
from config import ConfigKeys


def generate_filename(u) -> str:
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    return f"json_export_{u}_{date_time_str}.json"


def export_to_json(json_data,u):
    conf = current_app.config
    filename = generate_filename(u)
    file = f"{conf[ConfigKeys.APP_DOWNLOAD_DIRECTORY.value]}{os.path.sep}{filename}"
    with open(file, "w") as outfile:
        outfile.write(json_data)
    return filename
