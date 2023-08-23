import re
from flask import Flask, request, render_template, session, redirect, url_for, flash

from functions import SQLiteDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '1134124wefduhfsgiushdfuji'
db = SQLiteDB("dish.db")


@app.route('/cart', methods=['GET', 'PUT'])
def cart():  # put application's code here
    return "cart"


@app.route('/cart/order', methods=['POST'])
def order():  # put application's code here
    return "ordering"


@app.route('/cart/add', methods=['POST'])
def added():  # put application's code here
    return "add dishes in cart"


@app.route('/user', methods=['GET', 'DELETE'])
def user():  # put application's code here
    with SQLiteDB('dish.db') as db:
        user = db.select_from("user", ["*"], where=dict(id=session['user_id']))

    return render_template('user.html', user=user)


@app.route('/user/register', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        phone = re.sub(r'\D', '', request.form.get('phone', ''))
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        if all([phone, email, password1]) and password1 == password2:
            with SQLiteDB('dish.db') as db:
                db.insert_into("user", params=dict(Telephone=phone, Email=email, Password=password1))
                return redirect(url_for('user_signin'))

    return render_template('register.html')


@app.route('/user/sign_in', methods=['GET', 'POST'])
def user_signin():  # put application's code here

    if request.method == 'POST':
        phone = re.sub(r'\D', '', request.form.get('phone',''))
        password1 = request.form.get('password1')

        with SQLiteDB('dish.db') as db:
            user = db.select_from("user", ["*"], where=dict(Telephone=phone))
            if user:
                user = user[0]
                if user.get('Password') == password1:
                    session['user_id'] = user.get('ID')
                    return redirect(url_for('user'))
                else:
                    flash('Введенный пароль не является корректным', 'error')

    context = dict(
        title='hello word'
    )
    return render_template('sign_in.html', **context)


@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.pop('user.id')
    return redirect(url_for('user_signin'))


@app.route('/user/restore', methods=['POST'])
def user_restore():  # put application's code here
    return "reset password"


@app.route('/user/orders', methods=['GET'])
def user_history():  # put application's code here
    with SQLiteDB('dish.db') as db:
        orders = db.select_from("order", ["*"])
    return render_template('orders.html', orders=orders)


@app.route('/user/orders/<id>', methods=['GET'])
def user_history_id(id):  # put application's code here
    with SQLiteDB('dish.db') as db:
        order = db.select_from("order", ["*"], where=dict(id=id))
    return render_template('order.html', order=order)


@app.route('/user/address', methods=['GET', 'POST'])
def user_address():  # put application's code here
    if request.method == 'POST':
        city = request.form.get('city')
        street = request.form.get('street')
        house = request.form.get('house')
        apartment = request.form.get('apartment', 0)
        entrance = request.form.get('entrance', 0)
        floor = request.form.get('floor', 0)

        if all([city, street, house]):
            with SQLiteDB('dish.db') as db:
                db.insert_into('address', dict(city=city, street=street,house=house,apartment=apartment,entrance=entrance,floor=floor,User=session['user_id']))

    with SQLiteDB('dish.db') as db:
        addresses = db.select_from("address", ["*"], where=dict(User=session['user_id']))
    return render_template('address.html', addreses=addresses)


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_address_id(id):  # put application's code here
    with SQLiteDB('dish.db') as db:
        address = db.select_from("address", ["*"], where=dict(id=id, User=session['user_id']))
    return render_template('add.html', address=address)


@app.route('/menu', methods=['GET'])
def menu():  # put application's code here
    with SQLiteDB('dish.db') as db:
        dishes = db.select_from("dish", ["*"])

    return render_template('menu.html', dishes=dishes)


@app.route('/menu/<cat_name>', methods=['GET'])
def menu_category(cat_name):  # put application's code here
    with SQLiteDB('dish.db') as db:
        category = db.select_from("category", ["*"], where=dict(name=cat_name))
    return render_template('category.html', category=category)


@app.route('/menu/<cat_name>/<dish>', methods=['GET'])
def menu_cat_dish(dish):  # put application's code here
   with SQLiteDB('dish.db') as db:
        dish = db.select_from("dish", ["*"], where=dict(name=dish))
    return render_template('dish.html', dish=dish)


@app.route('/menu/search', methods=['GET'])
def menu_search():  # put application's code here
    search_query = request.args.get('search_query', '').strip()
    with SQLiteDB('dish.db') as db:
        dishes = db.sql_query(f'''SELECT * from dish WHERE dish.Dish_name LIKE "%{search_query}%"''')
    return render_template('search.html', dishes=dishes)


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():
    with SQLiteDB('dish.db') as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            db.insert_into("dish", data)
    return "list from dishes"


@app.route('/admin/dishes/<dish>', methods=['GET', 'PUT', 'DELETE'])
def edit_dish():  # put application's code here
    return "edit the dish"


@app.route('/admin/orders', methods=['GET'])
def admin_all_orders():  # put application's code here
    return "all orders"


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


if __name__ == '__main__':
    app.run()
