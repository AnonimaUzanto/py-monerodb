import json

from datetime import datetime


def varint_decoder(data):
    """https://github.com/fmoo/python-varint/blob/master/varint.py"""
    shift = 0
    result = 0
    idx = 0
    while True:
        i = data[idx]
        idx = idx + 1
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return idx, result


def read_json_from_file(filename: str) -> json:
    with open(filename) as file:
        data = json.load(file)
    return data


def pretty_print(data: dict):
    print(json.dumps(data, indent=4))


def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S UTC")
