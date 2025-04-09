from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Category, Item, Department, IssuedItem, Transaction
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'your_secret_key'

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if 'user' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('register.html', users=users)

@app.route('/register/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'])
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('register'))
    return render_template('edit_user.html', user=user)

@app.route('/register/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('manage_categories'))
    return render_template('edit_category.html', category=category)

@app.route('/categories/delete/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('manage_categories'))

@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        quantity = int(request.form['quantity'])
        purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d')

        # Check if item already exists
        item = Item.query.filter_by(name=name, category_id=category_id).first()
        if item:
            item.quantity += quantity
        else:
            item = Item(name=name, category_id=category_id, quantity=quantity, purchase_date=purchase_date)
            db.session.add(item)
            db.session.commit()  # Commit to generate item.id

        # Log the transaction
        transaction = Transaction(item_id=item.id, transaction_type='Received', quantity=quantity, date=purchase_date, remarks='Purchased')
        db.session.add(transaction)
        db.session.commit()

    items = Item.query.all()
    categories = Category.query.all()
    return render_template('items.html', items=items, categories=categories)

@app.route('/items/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        item.name = request.form['name']
        item.category_id = request.form['category_id']
        item.quantity = int(request.form['quantity'])
        db.session.commit()
        return redirect(url_for('manage_items'))
    return render_template('edit_item.html', item=item, categories=categories)

@app.route('/items/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)

    # Delete associated transactions
    Transaction.query.filter_by(item_id=id).delete()

    # Delete the item
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('manage_items'))

@app.route('/departments', methods=['GET', 'POST'])
def manage_departments():
    if request.method == 'POST':
        name = request.form['name']
        department = Department(name=name)
        db.session.add(department)
        db.session.commit()
    departments = Department.query.all()
    return render_template('departments.html', departments=departments)

@app.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    department = Department.query.get_or_404(id)
    if request.method == 'POST':
        department.name = request.form['name']
        db.session.commit()
        return redirect(url_for('manage_departments'))
    return render_template('edit_department.html', department=department)

@app.route('/departments/delete/<int:id>', methods=['POST'])
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('manage_departments'))

@app.route('/issue', methods=['GET', 'POST'])
def issue_items():
    if request.method == 'POST':
        item_id = request.form['item_id']
        department_id = request.form['department_id']
        quantity = int(request.form['quantity'])
        issue_date = datetime.strptime(request.form['issue_date'], '%Y-%m-%d')
        remark = request.form.get('remark', '')

        # Update item quantity
        item = Item.query.get(item_id)
        if item.quantity >= quantity:
            item.quantity -= quantity
            issued_item = IssuedItem(item_id=item_id, department_id=department_id, issue_date=issue_date, quantity=quantity, remark=remark)
            db.session.add(issued_item)

            # Log the transaction
            transaction = Transaction(item_id=item_id, transaction_type='Issued', quantity=quantity, date=issue_date, remarks=remark)
            db.session.add(transaction)

            db.session.commit()
        else:
            return "Error: Not enough items in stock", 400

    items = Item.query.all()
    departments = Department.query.all()
    issued_items = IssuedItem.query.all()
    return render_template('issue.html', items=items, departments=departments, issued_items=issued_items)

@app.route('/dashboard')
def dashboard():
    total_categories = Category.query.count()
    total_items = Item.query.count()
    total_departments = Department.query.count()
    low_stock_items = Item.query.filter(Item.quantity <= 5).all()
    return render_template('dashboard.html', total_categories=total_categories, total_items=total_items, total_departments=total_departments, low_stock_items=low_stock_items)

@app.route('/report', methods=['GET', 'POST'])
def generate_report():
    ledger = []
    if request.method == 'POST':
        from_date = datetime.strptime(request.form['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(request.form['to_date'], '%Y-%m-%d')
        item_id = request.form.get('item_id')

        # Fetch transactions from the Transaction table
        query = Transaction.query.filter(Transaction.date.between(from_date, to_date))
        if item_id:
            query = query.filter(Transaction.item_id == item_id)

        transactions = query.all()
        item_balances = {}

        for transaction in transactions:
            item_name = transaction.item.name
            if item_name not in item_balances:
                item_balances[item_name] = 0

            if transaction.transaction_type == 'Received':
                item_balances[item_name] += transaction.quantity
            elif transaction.transaction_type == 'Issued':
                item_balances[item_name] -= transaction.quantity

            ledger.append({
                'date': transaction.date.strftime('%Y-%m-%d'),
                'item_name': item_name,
                'received_quantity': transaction.quantity if transaction.transaction_type == 'Received' else 0,
                'issued_quantity': transaction.quantity if transaction.transaction_type == 'Issued' else 0,
                'remaining_balance': item_balances[item_name],
                'remarks': transaction.remarks
            })

        # Sort ledger by date
        ledger.sort(key=lambda x: x['date'])

    items = Item.query.all()
    return render_template('report.html', ledger=ledger, items=items)

@app.route('/print_low_stock')
def print_low_stock():
    low_stock_items = Item.query.filter(Item.quantity <= 5).all()
    return render_template('print_low_stock.html', low_stock_items=low_stock_items)

if __name__ == '__main__':
    app.run(debug=True)
