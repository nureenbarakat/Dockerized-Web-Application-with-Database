
from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(name)

# MySQL configurations
db_config = {
    'host': 'host.docker.internal',  # Use host.docker.internal to access MySQL on the host machine
    'user': 'root',  # MySQL username (default is 'root' for XAMPP)
    'password': '',  # MySQL password (if any)
    'database': 'students_db',  # Name of the database
}

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

# Endpoint to fetch students data
@app.route('/students', methods=['GET'])
def get_students():
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(students)
    else:
        return jsonify({"error": "Failed to connect to MySQL database"}), 500

# Endpoint to add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    cgpa = data.get('cgpa')

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, cgpa) VALUES (%s, %s)", (name, cgpa))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Student added successfully"}), 201
    else:
        return jsonify({"error": "Failed to connect to MySQL database"}), 500

# Endpoint to render the index.html file
@app.route('/')
def index():
    return render_template('index.html')

if name == 'main':
    app.run(debug=True, host='0.0.0.0')