from flask import Flask, request, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root12345",  # Make sure the password is correct
    database="db"  # Make sure the database exists
)

        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM USER WHERE User_Name = %s AND User_Type = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return render_template('index.html', message="Login Successful")
            else:
                return render_template('login.html', error="Invalid Credentials")
        else:
            return "Database connection failed"
    return render_template('login.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        data = request.form
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO USER (User_Name, User_Type, User_Location, User_Contact, User_Registration_Date)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (data['name'], data['type'], data['location'], data['contact'], data['registration_date'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return render_template('register.html', message="User registered successfully")
        return "Database connection failed"
    return render_template('register.html')

# Route for task assignment
@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        data = request.form
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO VOLUNTEER_ASSIGNMENT (Volunteer_ID, Assigned_Task, Assigned_Location, Assignment_Date)
                VALUES (%s, %s, %s, %s)
            """
            values = (data['volunteer_id'], data['task'], data['location'], data['date'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return render_template('task.html', message="Task assigned successfully")
        return "Database connection failed"
    return render_template('task.html')

# Route for notifications
@app.route('/notification', methods=['GET', 'POST'])
def notification():
    if request.method == 'POST':
        data = request.form
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO EMERGENCY_ALERT (Incident_ID, Alert_Message, Alert_Date)
                VALUES (%s, %s, %s)
            """
            values = (data['incident_id'], data['alert_message'], data['alert_date'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return render_template('notification.html', message="Alert added successfully")
        return "Database connection failed"
    return render_template('notification.html')

# Route for tracking funds
@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        data = request.form
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO FUND_TRACKING (Fund_ID, User_ID, Allocation_Date, Amount_Allocated, Usage_Details)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (data['fund_id'], data['user_id'], data['allocation_date'], data['amount_allocated'], data['usage_details'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return render_template('tracking.html', message="Fund tracking record added successfully")
        return "Database connection failed"
    return render_template('tracking.html')

# Route for donations
@app.route('/donations', methods=['GET', 'POST'])
def donations():
    connection = create_connection()
    if connection:
        if request.method == 'POST':
            data = request.form
            cursor = connection.cursor()
            query = """
                INSERT INTO FUND_COLLECTION (Donor_Name, Fund_Amount, Donation_Date)
                VALUES (%s, %s, %s)
            """
            values = (data['donor_name'], data['fund_amount'], data['donation_date'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()

        # Fetch all donations
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM FUND_COLLECTION")
        donations = cursor.fetchall()
        cursor.close()
        return render_template('donations.html', donations=donations)
    return "Database connection failed"

# Route for distribution
@app.route('/distribution', methods=['GET', 'POST'])
def distribution():
    connection = create_connection()
    if connection:
        if request.method == 'POST':
            data = request.form
            cursor = connection.cursor()
            query = """
                INSERT INTO DELIVERY (User_ID, Rehabilitation_Center_ID, Commodity_Name, Commodity_Quantity, Delivery_Date)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (data['user_id'], data['center_id'], data['commodity_name'], data['commodity_quantity'], data['delivery_date'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()

        # Fetch all deliveries
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DELIVERY")
        deliveries = cursor.fetchall()
        cursor.close()
        return render_template('distribution.html', deliveries=deliveries)
    return "Database connection failed"

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
