import re
from flask import Flask, request, render_template, session, redirect, url_for, flash

from functions import SQLiteDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '1134124wefduhfsgiushdfuji'
db = SQLiteDB("dish.db")


@app.route('/cart', methods=['GET', 'PUT'])
def cart():
    if 'cart' not in session:
        session['cart'] = {}

    if request.method == 'PUT':
        data = request.json
        dish_id = data.get('dish_id')
        quantity = data.get('quantity', 1)

        if dish_id:
            if dish_id in session['cart']:
                session['cart'][dish_id] += quantity
            else:
                session['cart'][dish_id] = quantity

        return {"message": "Added to cart"}

    return render_template('cart.html', cart=session['cart'])

@app.route('/cart/order', methods=['POST'])
def order():
    # Процесс оформления заказа
    return "Ordering"


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.form
    dish_id = data.get('dish_id')
    quantity = data.get('quantity', 1)

    if 'cart' not in session:
        session['cart'] = {}

    if dish_id:
        if dish_id in session['cart']:
            session['cart'][dish_id] += quantity
        else:
            session['cart'][dish_id] = quantity

    return {"message": "Added to cart"}


@app.route('/user', methods=['GET', 'DELETE'])
def user_endpoint():
    if 'user_id' in session:
        with SQLiteDB('dish.db') as db:
            user = db.select_from("user", ["*"], where=dict(id=session['user_id']))
            return render_template('user.html', user=user)
    return redirect(url_for('user_signin'))


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
def user_signin():
    if request.method == 'POST':
        phone = re.sub('', r'\D', request.form.get('phone', ''))
        password1 = request.form.get('password1')

        with SQLiteDB('dish.db') as db:
            user = db.select_from("user", ["*"], where=dict(Telephone=phone))
            if user:
                user = user[0]
                if user.get('Password') == password1:
                    session['user_id'] = user.get('ID')
                    return redirect(url_for('user_endpoint'))
                else:
                    flash('Введенный пароль не является корректным', 'error')

    context = {
        "title": 'Hello user'
    }
    return render_template('sign_in.html', **context)


@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.pop('user_id', None)
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


@app.route('/menu/<cat_name>/<dish_name>', methods=['GET'])
def menu_cat_dish(cat_name, dish_name):
    with SQLiteDB('dish.db') as db:
        dish = db.select_from("dish", ["*"], where=dict(name=dish_name))
    return render_template('dish.html', dish=dish)


@app.route('/menu/search', methods=['GET'])
def menu_search():  # put application's code here
    search_query = request.args.get('search_query', '').strip()
    with SQLiteDB('dish.db') as db:
        dishes = db.sql_query(f'''SELECT * from dish WHERE dish.Dish_name LIKE "%{search_query}%"''')
    return render_template('search.html', dishes=dishes)


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():
    if request.method == 'POST':
        data = request.form.to_dict()
        with SQLiteDB('dish.db') as db:
            db.insert_into("dish", data)

    with SQLiteDB('dish.db') as db:
        dishes = db.select_from("dish", ["*"])

    return render_template('admin_dishes.html', dishes=dishes)


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_dish(dish_id):
    with SQLiteDB('dish.db') as db:
        if request.method == 'PUT':
            data = request.form.to_dict()
            db.update("dish", data, where=dict(id=dish_id))
        else:
            dish = db.select_from("dish", ["*"], where=dict(id=dish_id))
            if dish:
                return render_template('edit_dish.html', dish=dish[0])
    return "Блюдо не найдено", 404


@app.route('/admin/orders', methods=['GET'])
def admin_all_orders():
    with SQLiteDB('dish.db') as db:
        orders = db.select_from("order", ["*"])
    return render_template('admin_orders.html', orders=orders)


@app.route('/admin/orders/<order_id>', methods=['GET'])
def admin_order_page(order_id):
    with SQLiteDB('dish.db') as db:
        order = db.select_from("order", ["*"], where=dict(id=order_id))
    return render_template('admin_order.html', order=order)


@app.route('/admin/orders/<order_id>/status', methods=['POST'])
def admin_order_status_update(order_id):
    new_status = request.form.get('status')
    with SQLiteDB('dish.db') as db:
        db.update("order", {"Status": new_status}, where=dict(id=order_id))
    return "Статус заказа обновлен"


@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    with SQLiteDB('dish.db') as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            db.insert_into("category", data)
        categories = db.select_from("category", ["*"])
    return render_template('admin_categories.html', categories=categories)


@app.route('/admin/categories/<category_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_category(category_id):
    with SQLiteDB('dish.db') as db:
        if request.method == 'PUT':
            data = request.form.to_dict()
            db.update("category", data, where=dict(id=category_id))
        elif request.method == 'DELETE':
            db.delete("category", where=dict(id=category_id))
        else:
            category = db.select_from("category", ["*"], where=dict(id=category_id))
            if category:
                return render_template('edit_category.html', category=category[0])
    return "Категория не найдена", 404


if __name__ == '__main__':
    app.run()