# These 3 imports are necessary to develop with Python Flask
from flask import Flask
from flask import render_template
from flask import request
# Import the sqlite3 python package to manage the SQLite database.db
import sqlite3

# Declare the Flask app
app = Flask(__name__)

# Route for the Home Page
@app.route("/")
def home():
    return render_template('index.html')

# Route for the About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Route for the page used to Confirm before you Reset the database
@app.route("/confirm_db")
def confirm_db():
    return render_template("confirm_db.html")

# Route executed when you post from the button on the from in the confirm_db.html page 
@app.route("/db",methods = ['POST', 'GET'])
def reset_db():
    # Connect to the SQLite database.db
    conn = sqlite3.connect('database.db')
    # DROP the students table if it exists 
    conn.execute('DROP TABLE IF EXISTS students')
    # Commit to the SQL command
    conn.commit()
    # Create a new copy of the students table
    conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, state TEXT, zip TEXT)')
    # Close database connection
    conn.close()
    # Open the database.html page
    return render_template('database.html', success='success')

# Route for adding a new student
@app.route('/enternew')
def new_student():
   return render_template('student.html')

# Route for adding a new student record to the database when a POST request
# is received from clicking the submit button from the form on the student.html Page
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        # Get all data from form on student.html page. Store data in variables. 
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            state = request.form['state']
            zip = request.form['zip']
            # Connect to SQLite database.db
            with sqlite3.connect("database.db") as con:
                # Create a cursor data structure to hold the data from variables
                cur = con.cursor()
                # Execute the INSERT statement using data from variables
                cur.execute("INSERT INTO students (name,addr,city,state,zip)VALUES (?,?,?,?,?)",(nm,addr,city,state,zip) )            
                # Close the database connection
                con.commit()
                # Store a success message in a variable called msg
                msg = "Record successfully added"
        except:
            # Rollback INSERT if there is an error in the transaction
            con.rollback()
            # Store an error message in a variable called msg
            msg = "error in insert operation"
      
        finally:
            # Close the database connection
            con.close()
            # Navigate to result.html page and send msg data
            return render_template("result.html",msg = msg)

# Route used to show all records in the students table
@app.route('/list')
def list():
    # Connect to the SQLite database.db
   con = sqlite3.connect("database.db")
   # Prepare to collect rows of data from SQLite database.db
   con.row_factory = sqlite3.Row
   # Create a cursor data stucture to hold data collected from database.db rows
   cur = con.cursor()
   # Execute SQL statement to SELECT all rows of data from students table
   cur.execute("select * from students")
   # Get all records returned from the SELECT query and store them in the cursor
   rows = cur.fetchall() 
   # Send the data to the list.html Page
   return render_template("list.html",rows = rows)
