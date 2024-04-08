# database.py

import sqlite3
from flask import g
from datetime import datetime

# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Function to close the database connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize the database when the application starts
def init_db():
    db = get_db()
    cursor = db.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    surname TEXT,
                    status TEXT
                )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    building TEXT,
                    description TEXT,
                    boxes_number INTEGER,
                    issued BOOLEAN DEFAULT 0
                )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS issuances (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    key_id INTEGER,
                    issuance_time TEXT,
                    return_time TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees(id),
                    FOREIGN KEY (key_id) REFERENCES keys(id)
                )''')

    db.commit()
    cursor.close()

# Other database operations...
def get_all_employees():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    return employees

def add_employee(name, surname, status):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO employees (name, surname, status) VALUES (?, ?, ?)", (name, surname, status))
    db.commit()
    cur.close()

def delete_employee(employee_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    db.commit()
    cur.close()

def get_all_keys():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM keys")
    keys = cur.fetchall()
    cur.close()
    return keys

def add_key(name, building, description, boxes_number):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO keys (name, building, description, boxes_number) VALUES (?, ?, ?, ?)", (name, building, description, boxes_number))
    db.commit()
    cur.close()

def delete_key(key_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM keys WHERE id=?", (key_id,))
    db.commit()
    cur.close()

# Implement other database operations for keys and issuances

def issue_key(employee_id, key_id, issuance_time):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE keys SET issued=1 WHERE id=?", (key_id,))
    cur.execute("INSERT INTO issuances (employee_id, key_id, issuance_time) VALUES (?, ?, ?)", (employee_id, key_id, issuance_time))
    db.commit()
    cur.close()

def return_key(key_id, return_time):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE keys SET issued=0 WHERE id=?", (key_id,))
    cur.execute("UPDATE issuances SET return_time=? WHERE key_id=? AND return_time IS NULL", (return_time, key_id))
    db.commit()
    cur.close()

def issue_key(employee_id, key_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE keys SET issued=1 WHERE id=?", (key_id,))
    issuance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO issuances (employee_id, key_id, issuance_time) VALUES (?, ?, ?)", (employee_id, key_id, issuance_time))
    db.commit()
    cur.close()

# Function to mark a door key as returned
def return_key(key_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE keys SET issued=0 WHERE id=?", (key_id,))
    return_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE issuances SET return_time=? WHERE key_id=? AND return_time IS NULL", (return_time, key_id))
    db.commit()
    cur.close()