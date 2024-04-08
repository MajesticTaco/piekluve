# app.py

from flask import Flask, render_template, g, request, redirect
from database import get_all_employees, get_all_keys, add_employee, delete_employee, add_key, delete_key, get_db, close_db, init_db

app = Flask(__name__)

initialized = False

# Register functions to run before and after each request
@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    close_db()

# Initialize the database when the application starts
def initialize():
    global initialized
    if not initialized:
        init_db()
        initialized = True

# Define routes

@app.route('/')
def index():
    initialize()
    return render_template('index.html')

@app.route('/admin')
def admin():
    initialize()
    employees = get_all_employees()
    keys = get_all_keys()
    return render_template('admin.html', employees=employees, keys=keys)

@app.route('/user')
def user():
    initialize()
    employees = get_all_employees()
    keys = get_all_keys()
    return render_template('user.html', employees=employees, keys=keys)

# Add routes for CRUD operations

@app.route('/add_employee', methods=['POST'])
def add_employee_route():
    name = request.form['name']
    surname = request.form['surname']
    status = request.form['status']
    add_employee(name, surname, status)
    return redirect('/admin')

@app.route('/add_key', methods=['POST'])
def add_key_route():
    name = request.form['key_name']
    building = request.form['building']
    description = request.form['description']
    boxes_number = request.form['boxes_number']
    add_key(name, building, description, boxes_number)
    return redirect('/admin')

@app.route('/delete_employee/<int:employee_id>')
def delete_employee_route(employee_id):
    delete_employee(employee_id)
    return redirect('/admin')

@app.route('/delete_key/<int:key_id>')
def delete_key_route(key_id):
    delete_key(key_id)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
