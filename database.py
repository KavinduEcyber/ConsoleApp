import os
import json


def read_data(filename: str) -> dict:
    with open(file=filename, mode='r') as file:
        data = file.read()
        return json.loads(data)


def write_data(filename: str, content: str):
    with open(file=filename, mode='w') as file:
        file.write(content)
