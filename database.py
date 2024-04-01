import json


class InternalServerError(Exception):
    pass


def write_data(filename: str, data: dict):
    try:
        with open(filename, 'w') as file:
            file.write(json.dumps(data))
    except IOError:
        raise InternalServerError('Internal Server Error 002.')


def read_data(filename: str) -> dict:
    try:
        with open(filename, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise InternalServerError('Internal Server Error 001.')
