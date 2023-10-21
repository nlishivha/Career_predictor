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
        cursor.execute("SELECT userid FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()
        session['userid'] = user_id[0]
        conn.commit()
        conn.close()
        return redirect(url_for('Ebg'))
    return render_template('userinfo.html')

@app.route("/Ebg", methods=['GET', 'POST'])
def Ebg():
    if request.method == 'POST':
        # Handle educational background form submission and insert into the database
        conn = connect_to_database()
        cursor = conn.cursor()

        level = request.form['level']
        qualification = request.form['qualification']
        field = request.form['field']
        
        # Get the user's email from the session (you should have stored it during signup)
        userid = session.get('userid')

        # Insert the educational background data into the database
        cursor.execute("INSERT INTO educationalbackground (userid, level, qualification, field) VALUES (%s, %s, %s, %s)",
                       (userid, level, qualification, field))
        conn.commit()
        conn.close()
        return redirect(url_for('job'))

    return render_template('Ebg.html')


@app.route('/job', methods=['GET', 'POST'])
def job():
    if request.method == 'POST':
        conn = connect_to_database()
        cursor = conn.cursor()

        # Pushing job preferences from the webpage
        jobpreferences = request.form.getlist('job_name')

        # Insert the selected job preferences into the database
        userid = session.get('userid')

        for jobpreference in jobpreferences:
            cursor.execute("INSERT INTO userjobpreferences (userid, jobpreferencename) VALUES (%s, %s)",
                           (userid, jobpreference))

        conn.commit()
        conn.close()
        return redirect(url_for('skills'))  # You can change this to the appropriate URL

    # Fetch a list of available job preferences from the database to display in the form
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT job_name FROM jobpositions")
    available_jobpreferences = cursor.fetchall()
    conn.close()

    return render_template('job.html', available_jobpreferences=available_jobpreferences)  # Pass available_jobpreferences to the template


@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if request.method == 'POST':

        #Database connection
        conn = connect_to_database()
        cursor = conn.cursor()

        #Pushing skill from database to webpage
        skills = request.form.getlist('skill_name') 

        # Insert the selected skills into the database
        userid = session.get('userid')

        for skill in skills:
            cursor.execute("INSERT INTO user_skills (userid, skillname) VALUES (%s, %s)",
                           (userid, skillname))
        
        conn.commit()
        conn.close()
        return redirect(url_for('user_experience'))

    # Fetch a list of available skills from the database to display in the form
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT skill_name FROM skills")
    available_skills = cursor.fetchall()
    conn.close()

    return render_template('skills.html', available_skills=available_skills)


@app.route('/user_experience', methods=['GET', 'POST'])
def user_experience():
    if request.method == 'POST':
        # Process the submitted form data
        experiences = request.form.getlist('experience')
        durations = request.form.getlist('duration')

        # Assuming you have user ID stored in the session
        userid = session.get('userid')

        conn = connect_to_database()
        cursor = conn.cursor()

        for experience, duration in zip(experiences, durations):
            # Insert the experience and duration into the database
            cursor.execute("INSERT INTO userexperience (userid, fieldname, experience) VALUES (%s, %s, %s)",
                           (userid, duration, experience))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))  # Replace 'next_page' with the actual URL

    return render_template('Userexperience.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
