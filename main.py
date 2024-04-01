import json

import database as db


class ValidationError(Exception):
    pass


class Admin:
    def __init__(self, name: str, password: str):
        data = db.read_data('users.txt')
        if name in data['admin']:
            if data['admin'][name] == password:
                print('Admin Log in Success.')
            else:
                raise ValidationError("User Name And Password Invalid!")
        else:
            raise ValidationError("User Name And Password Invalid!")

    def add_equipment(self, name: str, qty: int, price: float):
        try:
            equipments = db.read_data("equipment.txt")
            equipments['equipments'][name] = {
                "price": price,
                "count": qty,
            }
            db.write_data(filename='equipment.txt', data=equipments)
            print("New Equipment Add Successful!")
        except FileNotFoundError:
            print('Error: Internal Server Error 001.')

    def all_equipment(self):
        try:
            equipments = db.read_data("equipment.txt")
            for equipment in equipments['equipments']:
                print('Equipment name:', equipment, ' | Qty:', equipments['equipments'][equipment]['count'],' | Price:', equipments['equipments'][equipment]['price'])
        except FileNotFoundError:
            print('Error: Internal Server Error 001.')


if __name__ == '__main__':
    try:
        admin = Admin(name='admin', password='123456')
        admin.add_equipment(name="hello", qty=12, price=25.00)
        admin.all_equipment()
    except db.InternalServerError as error:
        print('Error:', error)
    except ValidationError as error:
        print('Error:', error)
