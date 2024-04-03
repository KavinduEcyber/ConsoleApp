import database as db
import json
import uuid

admin_file = 'admin.txt'
store_file = 'store.txt'
repair_file = 'repair.txt'
user_file = 'users.txt'
invoice_file = 'invoice.txt'


class CustomError(Exception):
    pass


class Common:
    def all_items(self):
        items = db.read_data(store_file)
        for item in items:
            print(item, items[item]['qty'], items[item]['price'])


class Admin(Common):
    def __init__(self, username: str, password: str):
        try:
            users = db.read_data(filename=admin_file)
            if username in users:
                if users[username] == password:
                    print('Hello Admin Login Success...!')
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

    def update_item(self, name: str, update: str, new):
        items = db.read_data(store_file)
        items[name][update] = new
        db.write_data(filename=store_file, content=json.dumps(items))
        print(name, update, 'is Updated to', new)

    def add_user(self, username: str, password: str):
        users = db.read_data(user_file)
        users[username] = password
        db.write_data(filename=user_file, content=json.dumps(users))
        print('New User', username, 'Add Success')


class User(Common):
    def __init__(self, username: str, password: str):
        try:
            users = db.read_data(filename=user_file)
            if username in users:
                if users[username] == password:
                    self.username = username
                    print('Hello Customer Login Success...!')
                else:
                    raise CustomError('Validation Error: UserName Or Password Incorrect!')
            else:
                raise CustomError('Validation Error: UserName Or Password Incorrect!')
        except FileNotFoundError:
            raise CustomError('Internal Server Error: Users Not Defined')

    def buy_item(self, name: str, qty: int, ):
        items = db.read_data(store_file)
        if name in items:
            if qty <= items[name]['qty']:
                invoices = db.read_data(invoice_file)
                invoices[self.username][name] = {"qty": qty, "price": int(items[name]['price']) * qty}
                db.write_data(filename=invoice_file, content=json.dumps(invoices))
                items = db.read_data(store_file)
                items[name]['qyt'] = int(items[name]['qyt']) - qty
                db.write_data(filename=store_file, content=json.dumps(items))
                print('Buy Success...')
            else:
                raise CustomError('Item Not Found: Quantity Not Available...!')
        else:
            raise CustomError('Item Not Found: ' + name + ' Not Found...!')


if __name__ == '__main__':
    print('Welcome To E-TEC BME Bio-Medical Equipment')
    user_type = str(input("Please Enter User Type 'admin' or 'customer' : ").lower())
    if user_type == 'admin':
        username = input('Enter Admin User Name : ')
        password = input('Enter User Password : ')
        try:
            admin = Admin(username=username, password=password)
            while True:
                choice = int(input(
                    '\n[0] Search Item \n[1] All Items \n[2] Add Item \n[3] Update Item \n[4] Add New User \n[5] Exit \nEnter Your Choice : '))
                if choice == 1:
                    print('')
                    admin.all_items()
                elif choice == 2:
                    item = input('Enter New Item Name : ')
                    qty = int(input('Enter Item Qty : '))
                    price = float(input('Enter Item price : '))
                    admin.add_items(name=item, qty=qty, price=price)
                elif choice == 4:
                    username = input('Enter New User  UserName : ')
                    password = input('Enter New User Password : ')
                    admin.add_user(username=username, password=password)
                elif choice == 5:
                    print('Exiting...')
                    break
                else:
                    print('Invalid Choice')
        except CustomError as error:
            print(error)
    elif user_type == 'customer':
        username = input('Enter Customer User Name : ')
        password = input('Enter User Password : ')
        try:
            user = User(username=username, password=password)
            while True:
                choice = int(input(
                    '\n[0] Search Item \n[1] All Items \n[2] Buy Item \n[3] Return Item \n[5] Exit \nEnter Your Choice : '))
                if choice == 0:
                    pass
                elif choice == 1:
                    print('')
                    user.all_items()
                elif choice == 2:
                    item_name = input("Enter Item Name : ")
                    item_qty = int(input("Enter Item Quantity : "))
                    user.buy_item(name=item_name, qty=item_qty)
                elif choice == 5:
                    print('Exiting...')
                    break
                else:
                    print('Invalid Choice')

        except CustomError as error:
            print(error)
    else:
        print('User Type', user_type, 'Not Available!')
