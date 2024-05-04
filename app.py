# importē nepieciešamās bibliotēkas
import serial
from serial.serialutil import SerialException
from flask import Flask, render_template, g, request, redirect, session
from database import get_all_employees, get_all_keys, add_employee, delete_employee, add_key, delete_key, get_db, close_db, init_db

# inicializē flask lietotni
app = Flask(__name__)
app.secret_key = 'tava_slēptā_atslēga_te'

initialized = False
rfid_port = 'COM10'

# izveido savienojumu ar datu bāzi pirms katras pieprasījuma
@app.before_request
def before_request():
    g.db = get_db()

# aizver datu bāzes savienojumu pēc katras pieprasījuma
@app.teardown_request
def teardown_request(exception):
    close_db()

# funkcija, lai inicializētu datu bāzi, ja tā vēl nav
def initialize():
    global initialized
    if not initialized:
        init_db()
        initialized = True

# mēģina izveidot savienojumu ar rfid lasītāju
try:
    rfid_reader = serial.Serial(rfid_port, 9600, timeout=0.1)
except SerialException as e:
    print("kļūda, atverot sērijas portu:", e)
    rfid_reader = None

# sākumlapas maršruts
@app.route('/')
def index():
    initialize()
    return render_template('index.html')

# pieteikšanās maršruts
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin_password':
            session['username'] = username
            return redirect('/admin')
        elif username == 'user' and password == 'user_password':
            session['username'] = username
            return redirect('/user')
        else:
            return 'nederīgs lietotājvārds vai parole'
    
    return render_template('login.html')

# izrakstīšanās maršruts
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# administrācijas lapas maršruts
@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == 'admin':
        initialize()
        employees = get_all_employees()
        keys = get_all_keys()
        return render_template('admin.html', employees=employees, keys=keys)
    else:
        return redirect('/login')

# lietotāja lapas maršruts
@app.route('/user')
def user():
    if 'username' in session and session['username'] == 'user':
        initialize()
        employees = get_all_employees()
        keys = get_all_keys()
        return render_template('user.html', employees=employees, keys=keys)
    else:
        return redirect('/login')

# pievieno darbinieku maršrutu
@app.route('/add_employee', methods=['POST'])
def add_employee_route():
    if 'username' in session and session['username'] == 'admin':
        name = request.form['name']
        surname = request.form['surname']
        status = request.form['status']
        add_employee(name, surname, status)
        return redirect('/admin')
    else:
        return redirect('/login')

# pievieno atslēgu maršrutu
@app.route('/add_key', methods=['POST'])
def add_key_route():
    if 'username' in session and session['username'] == 'admin':
        name = request.form['key_name']
        building = request.form['building']
        description = request.form['description']
        boxes_number = request.form['boxes_number']
        add_key(name, building, description, boxes_number)
        return redirect('/admin')
    else:
        return redirect('/login')

# pievieno atslēgu ar rfid maršrutu
@app.route('/add_key_rfid', methods=['POST'])
def add_key_rfid():
    if 'username' in session and session['username'] == 'admin':
        if rfid_reader:
            rfid_data = rfid_reader.readline().strip().decode('utf-8')
            if rfid_data:
                name = request.form['key_name']
                building = request.form['building']
                description = request.form['description']
                boxes_number = request.form['boxes_number']
                add_key(name, building, description, boxes_number)
                return redirect('/admin')
            else:
                return "kļūda: rfid dati ir tukši"
        else:
            name = request.form['key_name']
            building = request.form['building']
            description = request.form['description']
            boxes_number = request.form['boxes_number']
            add_key(name, building, description, boxes_number)
            return redirect('/admin')
    else:
        return redirect('/login')

# dzēst darbinieku maršrutu
@app.route('/delete_employee/<int:employee_id>')
def delete_employee_route(employee_id):
    if 'username' in session and session['username'] == 'admin':
        delete_employee(employee_id)
        return redirect('/admin')
    else:
        return redirect('/login')

# dzēst atslēgu maršrutu
@app.route('/delete_key/<int:key_id>')
def delete_key_route(key_id):
    if 'username' in session and session['username'] == 'admin':
        delete_key(key_id)
        return redirect('/admin')
    else:
        return redirect('/login')

# palaiž lietotni
if __name__ == '__main__':
    app.run(debug=True)
