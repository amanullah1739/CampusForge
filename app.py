from flask import Flask, render_template

app = Flask(__name__)

# ==========================
# Authentication
# ==========================

@app.route("/")
@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/signup")
def signup():
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


if __name__ == "__main__":
    app.run(debug=True)