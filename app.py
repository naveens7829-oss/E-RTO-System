from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
import re
import random

otp_storage = {}

app = Flask(__name__)
app.secret_key = "secret"

# Upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Database connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME ----------------
@app.route('/send_otp', methods=['POST'])
def send_otp():
    mobile = request.form['mobile']

    otp = str(random.randint(1000, 9999))
    otp_storage[mobile] = otp

    print("OTP for", mobile, "is:", otp)  # shown in terminal

    return "OTP Sent"

@app.route('/')
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        otp = request.form['otp']

        # Verify OTP
        if mobile not in otp_storage or otp_storage[mobile] != otp:
            return "Invalid OTP"

        db = get_db()
        db.execute(
            "INSERT INTO users(name,username,password,mobile) VALUES(?,?,?,?)",
            (name, username, password, mobile)
        )
        db.commit()

        return redirect('/login')

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (request.form['username'], request.form['password'])
        ).fetchone()

        if user:
            session['user'] = request.form['username']
            return redirect('/dashboard')

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
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

# ---------------- APPLY DL ----------------
@app.route('/apply_dl', methods=['GET','POST'])
def apply_dl():
    if request.method == 'POST':
        file = request.files['doc']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db = get_db()
        db.execute(
            "INSERT INTO dl_applications(name,age,doc,status,user) VALUES(?,?,?,?,?)",
            (request.form['name'], request.form['age'], filename, "Pending", session['user'])
        )
        db.commit()
        return redirect('/status')

    return render_template("apply_dl.html")

# ---------------- STATUS ----------------
@app.route('/status')
def status():
    db = get_db()
    data = db.execute("SELECT * FROM dl_applications").fetchall()
    return render_template("status.html", data=data)

# ---------------- ADMIN LOGIN ----------------
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

# ---------------- ADMIN PANEL ----------------
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    data = db.execute("SELECT * FROM dl_applications").fetchall()
    return render_template("admin.html", data=data)

# ---------------- UPDATE DL STATUS ----------------
@app.route('/update/<int:id>/<status>')
def update(id, status):
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    db.execute("UPDATE dl_applications SET status=? WHERE id=?", (status, id))
    db.commit()
    return redirect('/admin')

# ---------------- VEHICLE REGISTRATION ----------------
@app.route('/vehicle_reg', methods=['GET','POST'])
def vehicle_reg():
    if request.method == 'POST':
        vehicle_no = request.form['vehicle_no']

        pattern = r'^[A-Z]{2} [0-9]{2} [A-Z]{2} [0-9]{4}$'
        if not re.match(pattern, vehicle_no):
            return "Invalid format (Use: AA 00 AA 0000)"

        db = get_db()
        db.execute(
            "INSERT INTO vehicles(owner,vehicle_no,model,status) VALUES(?,?,?,?)",
            (request.form['owner'], vehicle_no, request.form['model'], "Pending")
        )
        db.commit()

        return redirect('/vehicle_list')

    return render_template("vehicle_reg.html")

# ---------------- VEHICLE LIST (ADMIN) ----------------
@app.route('/vehicle_list')
def vehicle_list():
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()

    # 👉 THIS IS THE LINE YOU ASKED
    data = db.execute("SELECT * FROM vehicles").fetchall()

    return render_template("vehicle_list.html", data=data)

# ---------------- VEHICLE APPROVE/REJECT ----------------
@app.route('/vehicle_update/<int:id>/<status>')
def vehicle_update(id, status):
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    db.execute("UPDATE vehicles SET status=? WHERE id=?", (status, id))
    db.commit()
    return redirect('/vehicle_list')

# ---------------- DASHBOARD AUTO DATA ----------------
@app.route('/dashboard_data')
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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "No message received"})

    user_msg = data["message"].lower()

    # Smart replies
    if "dl" in user_msg:
        reply = "Go to Apply DL section and fill the form."
    elif "vehicle" in user_msg:
        reply = "Use Vehicle Registration to register your vehicle."
    elif "status" in user_msg:
        reply = "Check your status in the Status page."
    elif "hello" in user_msg or "hi" in user_msg:
        reply = "Hello! How can I help you?"
    else:
        reply = "I understand your query. Please navigate through the dashboard options or contact admin."

    return jsonify({"reply": reply})

# ---------------- FEEDBACK ----------------
@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO feedback(name,message) VALUES(?,?)",
            (request.form['name'], request.form['message'])
        )
        db.commit()
        return "Feedback submitted successfully!"

    return render_template('feedback.html')

# ---------------- COMPLAINT ----------------
@app.route('/complaint', methods=['GET','POST'])
def complaint():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO complaints(name,complaint,status) VALUES(?,?,?)",
            (request.form['name'], request.form['complaint'], "Pending")
        )
        db.commit()
        return "Complaint submitted!"

    return render_template('complaint.html')

# ---------------- VIEW COMPLAINTS (ADMIN) ----------------
@app.route('/view_complaints')
def view_complaints():
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    data = db.execute("SELECT * FROM complaints").fetchall()
    return render_template('view_complaints.html', data=data)

@app.route('/logout')
def logout():

    # remove user session
    session.pop('user', None)

    # remove admin session
    session.pop('admin', None)

    return redirect('/login')


# ---------------- DATABASE INIT ----------------
def init_db():
    db = get_db()
    try:
        db.execute("ALTER TABLE users ADD COLUMN mobile TEXT")
    except:
        pass

    try:
        db.execute("ALTER TABLE dl_applications ADD COLUMN user TEXT")
    except:
        pass   # already exists, ignore

    db.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        message TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        complaint TEXT,
        status TEXT
    )
    """)

    db.commit()
    db.close()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

if __name__ == "__main__":
    app.run()