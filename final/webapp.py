from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2

app = Flask(__name__, template_folder="templates")

# Database configuration
DB_HOST = "intern2301-06-bridging-career-gaps-a.ctgb19tevqci.eu-west-1.rds.amazonaws.com"
DB_PORT = 5432
DB_DATABASE = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "BestTeam420"

# Set up a secret key for Flask (replace with a strong, random key)
app.secret_key = 'your_secret_key'

# Database connection
def connect_to_database():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
    )
# Add this route to your Flask application
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle registration form submission and database insert
        conn = connect_to_database()
        cursor = conn.cursor()

        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists based on email
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash("An account with this email already exists. Please use a different email.")
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)",
                           (email, password))
            conn.commit()
            conn.close()
            # Redirect to a valid route, e.g., 'userinfo'
            session['email'] = email  
            return redirect(url_for('userinfo'))

    return render_template('signup.html')

@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if request.method == 'POST':
        # Handle user information form submission and update the database
        conn = connect_to_database()
        cursor = conn.cursor()

        gender = request.form['gender']
        username = request.form['username']
        
        # Get the user's email from the session (you should have stored it during signup)
        email = session.get('email')

        # Update the user's information in the database
        cursor.execute("UPDATE users SET gender = %s, username = %s WHERE email = %s",
                       (gender, username, email))
        conn.commit()
        conn.close()
        return redirect(url_for('Ebg'))

    return render_template('userinfo.html')

@app.route("/Ebg", methods=['GET', 'POST'])
def Ebg():
    return render_template('Ebg.html')

@app.route('/ebg', methods=['GET', 'POST'])
def ebg():
    if request.method == 'POST':
        # Handle educational background form submission and insert into the database
        conn = connect_to_database()
        cursor = conn.cursor()

        level = request.form['level']
        qualification = request.form['qualification']
        field = request.form['field']
        
        # Get the user's email from the session (you should have stored it during signup)
        email = session.get('email')

        # Insert the educational background data into the database
        cursor.execute("INSERT INTO educationalbackground (email, level, qualification, field) VALUES (%s, %s, %s, %s)",
                       (email, level, qualification, field))
        conn.commit()
        conn.close()
        return redirect(url_for('user_dashboard'))

    return render_template('ebg.html')

if __name__ == '__main__':
    app.run(debug=True)
