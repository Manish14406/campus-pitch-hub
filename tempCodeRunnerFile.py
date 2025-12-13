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

# ROUTES
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit-pitch')
def submit_pitch():
    return render_template("submit_pitch.html")

@app.route('/pitch-submit-form')
def pitch_form():
    if "student_email" not in session:
        return redirect("/submit-pitch")

    return render_template("pitch_form.html")




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


# RUN SERVER + CREATE DB
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


