import database as db


class ValidationError(Exception):
    pass


class Admin:
    def __init__(self, name: str, password: str):
        try:
            data = db.read_data('users.txt')
            if name in data['admin']:
                if data['admin'][name] == password:
                    print('Admin Log in Success.')
                else:
                    raise ValidationError("User Name And Password Invalid!")
            else:
                raise ValidationError("User Name And Password Invalid!")
        except FileNotFoundError:
            print('Error: Internal Server Error 001.')

    def add_equipment(self, name: str, qty: int, price: float):
        try:
            equipments = db.read_data('equipment.txt')
            equipments[name] = {
                "price": qty,
                "count": price,
            }
            db.write_data(filename='equipment.txt', data=str(equipments))
        except FileNotFoundError:
            print('Error: Internal Server Error 001.')


if __name__ == '__main__':
    try:
        admin = Admin(name='admin', password='123456')
        admin.add_equipment(name='hone', qty=12, price=32.50)
    except ValidationError as error:
        print('Error:', error)
