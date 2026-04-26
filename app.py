from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# SQL Server connection
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost\SQLEXPRESS;"   # change this to your SSMS server name
    "Database=StudentDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()


# -----------------------
# Login Page
# -----------------------
@app.route('/')
def login():
    return render_template("login.html")


# -----------------------
# Login Check
# -----------------------
@app.route('/login', methods=['POST'])
def login_check():

    username = request.form['username']
    password = request.form['password']

    # simple login (demo purpose)
    if username == "admin" and password == "1234":
        return redirect('/dashboard')
    else:
        return "Invalid Login"


# -----------------------
# Dashboard
# -----------------------
@app.route('/dashboard')
def dashboard():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template("dashboard.html", students=students)


# -----------------------
# Add Student
# -----------------------
@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name']
    course = request.form['course']
    marks = request.form['marks']

    cursor.execute(
        "INSERT INTO students (name,course,marks) VALUES (?,?,?)",
        (name, course, marks)
    )

    conn.commit()

    return redirect('/dashboard')


# -----------------------
# Search Student
# -----------------------
@app.route('/search')
def search():

    name = request.args.get('name')

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    students = cursor.fetchall()

    return render_template("search.html", students=students)


# -----------------------
# Delete Student
# -----------------------
@app.route('/delete/<int:id>')
def delete_student(id):

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect('/dashboard')


# -----------------------
# Logout
# -----------------------
@app.route('/logout')
def logout():
    return redirect('/')


# -----------------------
# Run App
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)