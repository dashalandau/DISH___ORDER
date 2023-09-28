import re
from flask import Flask, request, render_template, session, redirect, url_for, flash
from models.user import User
from models.category import Category
from models.order import Order
from models.order_dish import OrderDish
from models.dish import Dish
from models.address import Address
from database import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = '1134124wefduhfsgiushdfuji'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dish.db'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


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
    if 'user_id' not in session:
        return "Для размещения заказа вы должны быть авторизованы", 401

    cart = session.get('cart')
    if not cart:
        return "Ваша корзина пуста", 400

    # Создаем новый заказ
    order = Order(user_id=session['user_id'])
    db_session.add(order)
    db_session.commit()

    # Добавляем блюда в заказ
    for dish_id, quantity in cart.items():
        dish = Dish.query.get(dish_id)
        if dish:
            order_dish = OrderDish(order_id=order.id, dish_id=dish_id, quantity=quantity)
            db_session.add(order_dish)

    db_session.commit()

    # Очищаем корзину
    session.pop('cart')

    return "Заказ успешно размещен"


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
    print(session)
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
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
            user = User(telephone=phone, email=email, password=password1)
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('user_signin'))

    return render_template('register.html')


@app.route('/user/sign_in', methods=['GET', 'POST'])
def user_signin():
    if request.method == 'POST':
        phone = request.form.get('phone', '')
        password1 = request.form.get('password1')

        user = User.query.filter_by(telephone=int(phone)).first()
        print(user)
        if user and user.password == password1:
            session['user_id'] = user.id
            return redirect(url_for('user_endpoint'))
        else:
            flash('Введенний пароль не є коректним', 'error')

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
def user_history():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)


@app.route('/user/orders/<id>', methods=['GET'])
def user_history_id(id):
    order = Order.query.get(id)
    if not order:
        return "Заказ не найден", 404
    order_dishes = OrderDish.query.filter_by(order_id=id).all()
    return render_template('order.html', order=order, order_dishes=order_dishes)


@app.route('/user/address', methods=['GET', 'POST'])
def user_address():
    if request.method == 'POST':
        town = request.form.get('city')
        street = request.form.get('street')
        house = request.form.get('house')
        apartment = request.form.get('apartment', 0)
        floor = request.form.get('floor', 0)

        if all([city, street, house]):
            address = Address(city=city, street=street, house=house, apartment=apartment, floor=floor, user_id=session['user_id'])
            db_session.add(address)
            db_session.commit()

    addresses = Address.query.filter_by(user_id=session['user_id']).all()
    return render_template('address.html', addresses=addresses)


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_address_id(id):
    address = Address.query.get(id)
    if not address:
        return "Адрес не найден", 404

    if request.method == 'PUT':
        data = request.form.to_dict()
        for field, value in data.items():
            setattr(address, field, value)
        db_session.commit()
    elif request.method == 'DELETE':
        db_session.delete(address)
        db_session.commit()
    return render_template('add.html', address=address)


@app.route('/menu', methods=['GET'])
def menu():
    dishes = Dish.query.all()
    return render_template('menu.html', dishes=dishes)



@app.route('/menu/<cat_name>', methods=['GET'])
def menu_category(cat_name):
    category = Category.query.filter_by(name=cat_name).first()
    if category:
        dishes = Dish.query.filter_by(category_id=category.id).all()
        return render_template('category.html', category=category, dishes=dishes)
    else:
        return "Категория не найдена", 404



@app.route('/menu/<cat_name>/<dish_name>', methods=['GET'])
def menu_cat_dish(cat_name, dish_name):
    category = Category.query.filter_by(name=cat_name).first()
    if category:
        dish = Dish.query.filter_by(name=dish_name, category_id=category.id).first()
        if dish:
            return render_template('dish.html', dish=dish)
        else:
            return "Блюдо не найдено в выбранной категории", 404
    else:
        return "Категория не найдена", 404



@app.route('/menu/search', methods=['GET'])
def menu_search():
    search_query = request.args.get('search_query', '').strip()
    if search_query:
        dishes = Dish.query.filter(Dish.name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', dishes=dishes, search_query=search_query)
    else:
        return "Введите поисковый запрос", 400



@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():
    if request.method == 'POST':
        data = request.form.to_dict()
        dish = Dish(**data)
        db.session.add(dish)
        db.session.commit()

    dishes = Dish.query.all()
    return render_template('admin_dishes.html', dishes=dishes)



@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_dish(dish_id):
    dish = Dish.query.get(dish_id)

    if not dish:
        return "Блюдо не найдено", 404

    if request.method == 'PUT':
        data = request.form.to_dict()
        for field, value in data.items():
            setattr(dish, field, value)
        db.session.commit()
    else:
        return render_template('edit_dish.html', dish=dish)

    return "Блюдо обновлено"



@app.route('/admin/orders', methods=['GET'])
def admin_all_orders():
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)


@app.route('/admin/orders/<order_id>', methods=['GET'])
def admin_order_page(order_id):
    order = Order.query.get(order_id)
    if not order:
        return "Заказ не найден", 404
    return render_template('admin_order.html', order=order)


from models.order import Order  # Импортируйте модель Order


@app.route('/admin/orders/<order_id>/status', methods=['GET', 'POST'])
def admin_order_status_update(order_id):
    if request.method == 'POST':
        new_status = request.form.get('status')
        order = Order.query.get(order_id)
        if not order:
            return "Заказ не найден", 404
        order.status = new_status
        db_session.commit()
        return "Статус заказа обновлен"
    elif request.method == 'GET':
        return "Выполняется GET-запрос для получения статуса заказа"


@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            category = Category(name=name)
            db_session.add(category)
            db_session.commit()

    categories = db_session.query(Category).all()
    return render_template('admin_categories.html', categories=categories)


@app.route('/admin/categories/<category_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return "Категорія не знайдена", 404

    if request.method == 'PUT':
        name = request.form.get('name')
        if name:
            category.name = name
            db_session.session.commit()
    elif request.method == 'DELETE':
        db_session.session.delete(category)
        db_session.session.commit()
    return render_template('edit_category.html', category=category)


app.app_context().push()

if __name__ == '__main__':
    app.run()
