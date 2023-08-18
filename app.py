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
    return user


@app.route('/user/register', methods=['GET','POST'])
def user_registration():
    return "registration"


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
    if request.method == 'POST':
        city = request.form.get('city')
        street = request.form.get('street')
        house = request.form.get('house')
        apartment = request.form.get('apartment', 0)
        entrance = request.form.get('entrance', 0)
        floor = request.form.get('floor', 0)

        Проверка на обязательные поля

        with SQLiteDB('dish.db') as db:
            address = db.insert_into('address', dict(city=city, street=street,house=house,apartment=apartment,entrance=entrance,floor=floor,User=session['user_id']))

    with SQLiteDB('dish.db') as db:
        addresses = db.select_from("address", ["*"], where=dict(User=session['user_id']))
    return render_template('adress.html', addreses=addresses)


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_address_id(id):  # put application's code here
    with SQLiteDB('dish.db') as db:
        address = db.select_from("address", ["*"], where=dict(id=id, User=session['user_id']))
    return address


@app.route('/menu', methods=['GET'])
def menu():  # put application's code here
    with SQLiteDB('dish.db') as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            db.insert_into("dish", data)

        dishes = db.select_from("dish", ["*"])

    html_form = f"""
    <form method = "POST">
        <input text="text" name="name" placeholder="name">
        <input text="text" name="Price" placeholder="price">
        <input text="text" name="Description" placeholder="description">
        <input text="text" name="picture" placeholder="picture">
        <input text="text" name="category" placeholder="category">
        <input type="submit">
    </form>
    <br>
    {str(dishes)}
    """
    return html_form


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


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():  # put application's code here
    return "list from dishes"


@app.route('/admin/dishes/<dish>', methods=['GET', 'PUT', 'DELETE'])
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


if __name__ == '__main__':
    app.run()
