import os
import json
from flask import Response


BASE_DATA_DIR = "./sensor_data/logs"
BASE_IMAGE_DIR = "./sensor_data/images"

def get_data_dir():
    """
    Returns all the files in the data directory.
    """
    if not os.path.exists(BASE_DATA_DIR):
        os.makedirs(BASE_DATA_DIR)
    files = os.listdir(BASE_DATA_DIR)
    files = [f.removesuffix(".csv") for f in files if os.path.isfile(os.path.join(BASE_DATA_DIR, f))]
    return files

def get_data_file(filename):
    """
    Returns the contents of a data file.
    :param filename: The name of the file to read.
    :return: The contents of the file.
    """
    if not os.path.exists(BASE_DATA_DIR):
        os.makedirs(BASE_DATA_DIR)
    with open(os.path.join(BASE_DATA_DIR, filename + ".csv"), "r") as f:
        # convert into column based json
        d = {}
        keys = []
        for line in f:
            if not keys:
                keys = line.strip().split(",")
                for key in keys:
                    d[key] = []
            else:
                values = line.strip().split(",")
                for i, key in enumerate(keys):
                    d[key].append(values[i])
        return d

def get_image(filename):
    """
    Returns the contents of a data file.
    :param filename: The name of the file to read.
    :return: The Flask Response object with the image data.
    """
    if not os.path.exists(BASE_IMAGE_DIR):
        os.makedirs(BASE_IMAGE_DIR)
    if not os.path.isfile(os.path.join(BASE_IMAGE_DIR, filename + ".jpg")):
        return {"error": "File not found"}, 404
    
    with open(os.path.join(BASE_IMAGE_DIR, filename + ".jpg"), "rb") as f:
        image_data = f.read()
    response = Response(image_data, mimetype='image/jpeg')
    return response
