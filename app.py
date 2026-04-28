from flask import Flask, render_template, request, redirect, session
from flask import jsonify
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = "secret"

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        db=get_db()
        db.execute("INSERT INTO users(name,username,password) VALUES(?,?,?)",
                   (request.form['name'],request.form['username'],request.form['password']))
        db.commit()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        db=get_db()
        user=db.execute("SELECT * FROM users WHERE username=? AND password=?",
                        (request.form['username'],request.form['password'])).fetchone()
        if user:
            session['user']=request.form['username']
            return redirect('/dashboard')
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    db = get_db()
    data = db.execute("SELECT * FROM dl_applications").fetchall()

    total = len(data)
    pending = sum(1 for d in data if d[4] == 'Pending')
    approved = sum(1 for d in data if d[4] == 'Approved')
    rejected = sum(1 for d in data if d[4] == 'Rejected')

    return render_template(
        "dashboard.html",
        total=total,
        pending=pending,
        approved=approved,
        rejected=rejected
    )

@app.route('/apply_dl', methods=['GET','POST'])
def apply_dl():
    if request.method=='POST':
        file=request.files['doc']
        filename=file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        db=get_db()
        db.execute("INSERT INTO dl_applications(name,age,doc,status) VALUES(?,?,?,?)",
                   (request.form['name'],request.form['age'],filename,"Pending"))
        db.commit()
        return redirect('/status')
    return render_template("apply_dl.html")

@app.route('/status')
def status():
    db=get_db()
    data=db.execute("SELECT * FROM dl_applications").fetchall()
    return render_template("status.html",data=data)

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    data = db.execute("SELECT * FROM dl_applications").fetchall()
    return render_template("admin.html", data=data)

@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        db = get_db()
        admin = db.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (request.form['username'], request.form['password'])
        ).fetchone()

        if admin:
            session['admin'] = request.form['username']
            return redirect('/admin')

    return render_template("admin_login.html")

@app.route('/update/<int:id>/<status>')
def update(id,status):
    db=get_db()
    db.execute("UPDATE dl_applications SET status=? WHERE id=?", (status,id))
    db.commit()
    return redirect('/admin')

@app.route('/vehicle_reg', methods=['GET','POST'])

@app.route('/vehicle_reg', methods=['GET','POST'])
def vehicle_reg():
    if request.method == 'POST':

        vehicle_no = request.form['vehicle_no']

        # Pattern: AA 00 AA 0000
        pattern = r'^[A-Z]{2} [0-9]{2} [A-Z]{2} [0-9]{4}$'

        if not re.match(pattern, vehicle_no):
            return "Invalid Vehicle Number Format (Use: AA 00 AA 0000)"

        db = get_db()
        db.execute(
            "INSERT INTO vehicles(owner,vehicle_no,model,status) VALUES(?,?,?,?)",
            (request.form['owner'], vehicle_no, request.form['model'], "Pending")
        )
        db.commit()

        return redirect('/vehicle_list')

    return render_template("vehicle_reg.html")

    return render_template("vehicle_reg.html")

@app.route('/vehicle_list')

@app.route('/vehicle_list')
def vehicle_list():
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    data = db.execute("SELECT * FROM vehicles").fetchall()
    return render_template("vehicle_list.html", data=data)

@app.route('/dashboard_data')

@app.route('/vehicle_update/<int:id>/<status>')

@app.route('/vehicle_update/<int:id>/<status>')
def vehicle_update(id, status):
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    db.execute("UPDATE vehicles SET status=? WHERE id=?", (status, id))
    db.commit()
    return redirect('/vehicle_list')

@app.route('/vehicle_update')
def vehicle_update_error():
    return "Invalid Access"

def dashboard_data():
    db = get_db()
    data = db.execute("SELECT * FROM dl_applications").fetchall()

    total = len(data)
    pending = sum(1 for d in data if d[4] == 'Pending')
    approved = sum(1 for d in data if d[4] == 'Approved')
    rejected = sum(1 for d in data if d[4] == 'Rejected')

    return jsonify({
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected
    })

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)