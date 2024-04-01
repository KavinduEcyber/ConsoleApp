import json


def write_data(filename: str, data: str):
    try:
        with open(filename, 'w') as file:
            file.write(data)
    except IOError:
        print('Error: Internal Server Error 002.')


def read_data(filename: str) -> dict:
    with open(filename, 'r') as file:
        return json.loads(file.read())
