import os

import requests
from dotenv import load_dotenv

load_dotenv()
fb = os.getenv("FIREBASE_API")


def filter_name(data, name):
    filtered_data = {}
    if data:
        for i in data:
            if data[i]["name"] == name:
                filtered_data[i] = data[i]

    return filtered_data


def filter_server(data, server_id):
    filtered_data = {}
    # use filter
    if data:
        for i in data:
            if data.get(i).get("server") == server_id:
                filtered_data[i] = data[i]

    return filtered_data


def filter_url(data, url):
    filtered_data = {}
    if data:
        for i in data:
            if data.get(i).get("url") == url:
                filtered_data[i] = data[i]

    return filtered_data


def delete_cm(data):
    id_cm = list(data.keys())[0]
    r = requests.delete(f"{fb}/commands/{id_cm}.json")
    return r


def get_url(data):
    id_cm = list(data.keys())[0]
    r = requests.get(f"{fb}/commands/{id_cm}/url.json")
    return r.json()
