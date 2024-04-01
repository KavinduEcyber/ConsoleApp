import json

import database as db

user_file = 'admin.txt'
store_file = 'store.txt'
repair_file = 'repair.txt'


class CustomError(Exception):
    pass


class Admin:
    def __init__(self, username: str, password: str):
        try:
            users = db.read_data(filename=user_file)
            if username in users:
                if users[username] == password:
                    print('Login Success...!')
                else:
                    raise CustomError('Validation Error: UserName Or Password Incorrect!')
            else:
                raise CustomError('Validation Error: UserName Or Password Incorrect!')
        except FileNotFoundError:
            raise CustomError('Internal Server Error: Admins Not Defined')

    def add_items(self, name: str, qty: int, price: float):
        items = db.read_data(store_file)
        items[name] = {"qty": qty, "price": price}
        db.write_data(filename=store_file, content=json.dumps(items))
        print('New Item', name, 'Add...')

    def all_items(self):
        items = db.read_data(store_file)
        for item in items:
            print(item, items[item]['qty'], items[item]['price'])

    def update_item(self, name: str, update: str, new):
        items = db.read_data(store_file)
        items[name][update] = new
        db.write_data(filename=store_file, content=json.dumps(items))
        print(name, update, 'is Updated to', new)


try:
    admin = Admin(username='admin', password='password')
    admin.add_items(name='Iphone', qty=10, price=2052)
    admin.all_items()
    admin.update_item(name='Iphone', update='price', new=8000)
except CustomError as error:
    print(error)
