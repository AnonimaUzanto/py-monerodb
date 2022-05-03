import json


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


def pretty_print(data: dict):
    print(json.dumps(data, indent=4))
