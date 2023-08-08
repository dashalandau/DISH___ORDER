from flask import Flask, request

from functions import SQLiteDB

app = Flask(__name__)


@app.route('/cart', methods=['GET', 'PUT'])
def cart():  # put application's code here
    return "cart"


@app.route('/cart/order', methods=['POST'])
def order():  # put application's code here
    return "ordering"


@app.route('/cart/add', methods=['POST'])
def added():  # put application's code here
    return "add dishes in cart"


@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user():  # put application's code here
    with SQLiteDB('dish.db') as db:
        user = db.select_from("user", ["*"], where=dict(id=1))
    return user


@app.route('/user/register', methods=['POST'])
def user_registration():  # put application's code here
    return "registration"


@app.route('/user/sign_in', methods=['POST'])
def user_signin():  # put application's code here
    return "sign in profile"


@app.route('/user/logout', methods=['POST'])
def user_logout():  # put application's code here
    return "logout"


@app.route('/user/restore', methods=['POST'])
def user_restore():  # put application's code here
    return "reset password"


@app.route('/user/orders', methods=['GET'])
def user_history():  # put application's code here
    with SQLiteDB('dish.db') as db:
        orders = db.select_from("order", ["*"])
    return orders


@app.route('/user/orders/<id>', methods=['GET'])
def user_history_id(id):  # put application's code here
    with SQLiteDB('dish.db') as db:
        order = db.select_from("order", ["*"], where=dict(id=id))
    return order


@app.route('/user/address', methods=['GET', 'POST'])
def user_address():  # put application's code here
    with SQLiteDB('dish.db') as db:
        addresses = db.select_from("address", ["*"])
    return addresses


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_address_id(id):  # put application's code here
    with SQLiteDB('dish.db') as db:
        address = db.select_from("address", ["*"], where=dict(id=id))
    return address


@app.route('/menu', methods=['GET'])
def menu():  # put application's code here
    with SQLiteDB('dish.db') as db:
        dishes = db.select_from("dish", ["*"])
    return dishes


@app.route('/menu/<cat_name>', methods=['GET'])
def menu_category(cat_name):  # put application's code here
    with SQLiteDB('dish.db') as db:
        category = db.select_from("category", ["*"], where=dict(name=cat_name))
    return category


@app.route('/menu/<cat_name>/<dish>', methods=['GET'])
def menu_cat_dish():  # put application's code here
    return "dish in the category"


@app.route('/menu/<cat_name>/<dish>/review', methods=['POST'])
def menu_dish_review():  # put application's code here
    return "review dish"


@app.route('/menu/search', methods=['GET'])
def menu_search():  # put application's code here
    search_query = request.args.get('search_query', '').strip()
    with SQLiteDB('dish.db') as db:
        dishes = db.sql_query(f'''SELECT * from dish WHERE dish.Dish_name LIKE "%{search_query}%"''')
    return dishes


@app.route('/admin/dishes', methods=['GET'])
def admin_dishes():  # put application's code here
    return "list from dishes"


@app.route('/admin/dishes/<dish>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def edit_dish():  # put application's code here
    return "edit the dish"


@app.route('/admin/orders', methods=['GET'])
def admin_all_orders():  # put application's code here
    return "all orders"


@app.route('/admin/orders?status={new/in_progress}', methods=['GET'])
def admin_order_status():  # put application's code here
    return "new order/order in progress"


@app.route('/admin/orders/<id>', methods=['GET'])
def admin_order_page():  # put application's code here
    return "page order"


@app.route('/admin/orders/<id>/status', methods=['POST'])
def admin_order_status_update():  # put application's code here
    return "update status order"


@app.route('/admin/<cat_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def edit_category():  # put application's code here
    return "edit_category"


@app.route('/admin/search', methods=['GET'])
def search_name():  # put application's code here
    return "search for name"


if __name__ == 'main':
    app.run()