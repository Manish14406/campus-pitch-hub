# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, session, jsonify, redirect 


app = Flask(__name__)
app.secret_key = "mysecretkey"

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_pitch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE TABLE
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(120), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    pitch_title = db.Column(db.String(200), nullable=False)
    pitch_description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), default="Pending")  

# ROUTES
@app.route('/')
def home():
    approved_pitches = Pitch.query.filter_by(status="Approved").all()
    return render_template("index.html", approved_pitches=approved_pitches)

@app.route('/submit-pitch')
def submit_pitch():
    return render_template("submit_pitch.html")


@app.route('/add-sample-students')
def add_sample_students():

    for num in range(55, 116):  # 055 to 115
        roll_number = f"R24EJ{num:03d}"   # Formats like 055, 056...115
        email = f"{roll_number}@reva.edu.in"

        student = Student(email=email)
        db.session.add(student)
    db.session.commit()
    return "Sample REVA students R24EJ055 to R24EJ115 added!"

@app.route("/verify-email")
def verify_email():
    email = request.args.get("email")

    student = Student.query.filter_by(email=email).first()

    if student:
        session["student_email"] = email
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})
    
@app.route('/show-students')
def show_students():
    students = Student.query.all()
    return "<br>".join([s.email for s in students])

# ------------------ DEBUG ROUTE ------------------


@app.route('/debug/pitches')
def debug_pitches():
    if not session.get('admin'):
        return "ACCESS DENIED", 403

    pitches = Pitch.query.all()
    return "<br>".join([f"{p.id} | {p.full_name} | {p.pitch_title} | {p.status}" for p in pitches])





# -----------------Pitch form-------------------

@app.route('/pitch-submit-form', methods=["GET", "POST"])
def pitch_form():
    if "student_email" not in session:
        return redirect("/submit-pitch")

    if request.method == "POST":
        email = request.form['email']
        full_name = request.form['full_name']
        branch = request.form['branch']
        semester = request.form['semester']
        phone = request.form['phone']
        pitch_title = request.form['pitch_title']
        pitch_description = request.form['pitch_description']

        # Save to database
        new_pitch = Pitch(
            email=email,
            full_name=full_name,
            branch=branch,
            semester=semester,
            phone=phone,
            pitch_title=pitch_title,
            pitch_description=pitch_description
        )

        db.session.add(new_pitch)
        db.session.commit()

        return render_template("success.html", name=full_name)

    return render_template("pitch_form.html")

# ------------------ ADMIN PANEL ------------------
@app.route('/admin/pitches')
def admin_pitches():
    if not session.get('admin'):
        return redirect('/admin/login')

    pitches = Pitch.query.all()
    return render_template("admin_pitches.html", pitches=pitches)

@app.route('/admin/approve/<int:id>')
def approve_pitch(id):
    if not session.get('admin'):
        return redirect('/admin/login')

    pitch = Pitch.query.get(id)
    pitch.status = "Approved"
    db.session.commit()
    return redirect("/admin/pitches")

@app.route('/admin/reject/<int:id>')
def reject_pitch(id):
    if not session.get('admin'):
        return redirect('/admin/login')

    pitch = Pitch.query.get(id)
    pitch.status = "Rejected"
    db.session.commit()
    return redirect("/admin/pitches")


@app.route('/admin/delete/<int:id>')
def delete_pitch(id):
    if not session.get('admin'):
        return redirect('/admin/login')

    pitch = Pitch.query.get(id)

    if pitch:
        db.session.delete(pitch)
        db.session.commit()

    return redirect("/admin/pitches")


#--------------Admin login route--------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "manish_rai" and password == "manish@9402" :
            session['admin'] = True
            return redirect('/admin/pitches')
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin/login')


# RUN SERVER + CREATE DB
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)


