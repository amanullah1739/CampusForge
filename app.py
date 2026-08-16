from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from database import db, migrate
from database.models.user import User
from flask_bcrypt import Bcrypt



# =========================================
# CREATE FLASK APPLICATION
# =========================================

app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

bcrypt = Bcrypt(app)
#=============================
# DATABAASE
#=============================
db.init_app(app)
migrate.init_app(app,db)

# ==========================
# Authentication
# ==========================

@app.route("/")
@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        roll_number = request.form.get("roll_number")
        email = request.form.get("email")
        branch = request.form.get("branch")
        year = request.form.get("year")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        terms = request.form.get("terms")

        # =========================================
        # VALIDATION
        # =========================================

        if not all([
            full_name,
            roll_number,
            email,
            branch,
            year,
            password,
            confirm_password,
            terms
        ]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("signup"))

        # =========================================
        # CHECK EXISTING USER
        # =========================================

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("signup"))

        existing_roll = User.query.filter_by(
            roll_number=roll_number
        ).first()

        if existing_roll:
            flash("This roll number is already registered.", "error")
            return redirect(url_for("signup"))

        # =========================================
        # HASH PASSWORD
        # =========================================

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        # =========================================
        # CREATE USER
        # =========================================

        new_user = User(
            full_name=full_name,
            roll_number=roll_number,
            email=email,
            branch=branch,
            year=year,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # =========================================
        # SUCCESS
        # =========================================

        return redirect(url_for("login"))

    return render_template("auth/signup.html")

@app.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot-password.html")

@app.route("/otp")
def otp():
    return render_template("auth/otp.html")

@app.route("/reset-password")
def reset_password():
    return render_template("auth/reset-password.html")

@app.route("/success")
def success():
    return render_template("auth/success.html")

# ==========================
# Onboarding
# ==========================

@app.route("/welcome")
def welcome():
    return render_template("onboarding/welcome.html")


@app.route("/basic-info")
def basic_info():
    return render_template("onboarding/basic-info.html")


@app.route("/skills")
def skills():
    return render_template("onboarding/skills.html")


@app.route("/connect")
def connect():
    return render_template("onboarding/connect.html")


@app.route("/complete")
def complete():
    return render_template("onboarding/complete.html")


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")

# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(debug=True)