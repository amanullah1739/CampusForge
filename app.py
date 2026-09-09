from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from config import Config

from database import db, migrate

from database.models.user import User
from database.models.project import Project
from database.models.platform_account import PlatformAccount
from database.models.platform_stats import PlatformStats

from database.services.platforms.sync_service import (
    sync_codeforces_account
)

from database.services.platform_verification import (
    generate_verification_code,
    get_verification_expiry
)

from flask_bcrypt import Bcrypt

from authlib.integrations.flask_client import OAuth

from utils.decorators import admin_required


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)


# =========================================================
# EXTENSIONS
# =========================================================

bcrypt = Bcrypt(app)

oauth = OAuth(app)


# =========================================================
# CODEFORCES OAUTH CONFIGURATION
# =========================================================

oauth.register(
    name="codeforces",
    client_id=app.config["CODEFORCES_CLIENT_ID"],
    client_secret=app.config["CODEFORCES_CLIENT_SECRET"],
    server_metadata_url="https://codeforces.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid"
    }
)


# =========================================================
# DATABASE
# =========================================================

db.init_app(app)
migrate.init_app(app, db)


# =========================================================
# HOME / PUBLIC ROUTES
# =========================================================

@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================================================
# AUTHENTICATION
# =========================================================

# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        login_type = request.form.get(
            "login_type",
            "student"
        )

        # Find user
        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            flash(
                "Invalid email or password.",
                "error"
            )
            return redirect(url_for("login"))

        # Check password
        if not bcrypt.check_password_hash(
            user.password_hash,
            password
        ):
            flash(
                "Invalid email or password.",
                "error"
            )
            return redirect(url_for("login"))

        # Check selected login type
        if (
            login_type == "student"
            and user.role != "student"
        ):
            flash(
                "Please use Admin Login for this account.",
                "error"
            )
            return redirect(url_for("login"))

        if (
            login_type == "admin"
            and user.role != "admin"
        ):
            flash(
                "Please use Student Login for this account.",
                "error"
            )
            return redirect(url_for("login"))

        # Create session
        session["user_id"] = user.id

        # Redirect according to role
        if user.role == "admin":
            return redirect(
                url_for("admin_dashboard")
            )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "auth/login.html"
    )


# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# -------------------------
# SIGNUP
# -------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    

    if request.method == "POST":

        full_name = request.form.get("full_name")
        roll_number = request.form.get("roll_number")
        email = request.form.get("email")
        branch = request.form.get("branch")
        year = request.form.get("year")
        password = request.form.get("password")
        
        confirm_password = request.form.get(
            "confirm_password"
        )
        signup_type = request.form.get("signup_type", "student")
        college_id = request.form.get("college_id")
        print("SIGNUP TYPE:", signup_type)
        print("COLLEGE ID:", college_id)
        print("EMAIL:", email)
        terms = request.form.get("terms")

        # =========================================
        # VALIDATION
        # =========================================

        if signup_type == "student":

            if not all([
                full_name,
                roll_number,
                email,
                branch,
                year,
                password,
                confirm_password,
                terms,
                college_id
            ]):
                flash(
                    "Please fill in all student fields.",
                    "error"
                )
                return redirect(url_for("signup"))

        else:

            if not all([
                full_name,
                email,
                password,
                confirm_password,
                terms,
                college_id
            ]):
                flash(
                    "Please fill in all admin fields.",
                    "error"
                )
                return redirect(url_for("signup"))

            

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("signup")
            )

        # =========================================
        # CHECK EXISTING EMAIL
        # =========================================

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(
                url_for("signup")
            )

        # =========================================
        # CHECK EXISTING ROLL NUMBER
        # =========================================

        if signup_type == "student":

            existing_roll = User.query.filter_by(
                roll_number=roll_number
            ).first()

            if existing_roll:
                flash(
                    "This roll number is already registered.",
                    "error"
                )
                return redirect(
                    url_for("signup")
                )

        # =========================================
        # HASH PASSWORD
        # =========================================

        hashed_password = (
            bcrypt
            .generate_password_hash(password)
            .decode("utf-8")
        )

        # =========================================
        # CREATE USER
        # =========================================

        new_user = User(
            full_name=full_name,
            roll_number=roll_number,
            email=email,
            branch=branch,
            year=year,
            password_hash=hashed_password,
            college_id=int(college_id),
            role=signup_type
        )

        db.session.add(new_user)
        db.session.commit()

        # =========================================
        # SUCCESS
        # =========================================

        return redirect(
            url_for("login")
        )

    return render_template(
        "auth/signup.html"
    )


# -------------------------
# FORGOT PASSWORD
# -------------------------

@app.route("/forgot-password")
def forgot_password():

    return render_template(
        "auth/forgot-password.html"
    )


# -------------------------
# OTP
# -------------------------

@app.route("/otp")
def otp():

    return render_template(
        "auth/otp.html"
    )


# -------------------------
# RESET PASSWORD
# -------------------------

@app.route("/reset-password")
def reset_password():

    return render_template(
        "auth/reset-password.html"
    )


# -------------------------
# SUCCESS
# -------------------------

@app.route("/success")
def success():

    return render_template(
        "auth/success.html"
    )


# =========================================================
# ADMIN
# =========================================================

# -------------------------
# ADMIN DASHBOARD
# -------------------------

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    user = User.query.get(
        session["user_id"]
    )

    college = user.college

    # =========================================
    # TOTAL STUDENTS
    # =========================================

    total_students = User.query.filter_by(
        college_id=college.id,
        role="student"
    ).count()

    # =========================================
    # TOTAL PROJECTS
    # =========================================

    total_projects = Project.query.join(
        User,
        Project.user_id == User.id
    ).filter(
        User.college_id == college.id,
        User.role == "student"
    ).count()

    # =========================================
    # TOTAL PROBLEMS
    # =========================================

    total_problems = db.session.query(
        db.func.coalesce(
            db.func.sum(
                PlatformStats.unique_problems_solved
            ),
            0
        )
    ).join(
        PlatformAccount,
        PlatformStats.platform_account_id
        == PlatformAccount.id
    ).join(
        User,
        PlatformAccount.user_id
        == User.id
    ).filter(
        User.college_id == college.id,
        User.role == "student"
    ).scalar()

    # =========================================
    # TOTAL SUBMISSIONS
    # =========================================

    total_submissions = db.session.query(
        db.func.coalesce(
            db.func.sum(
                PlatformStats.total_submissions
            ),
            0
        )
    ).join(
        PlatformAccount,
        PlatformAccount.id
        == PlatformStats.platform_account_id
    ).join(
        User,
        PlatformAccount.user_id
        == User.id
    ).filter(
        User.college_id == college.id,
        User.role == "student"
    ).scalar()

    return render_template(
        "admin/dashboard.html",
        college=college,
        total_students=total_students,
        total_projects=total_projects,
        total_problems=total_problems,
        total_submissions=total_submissions
    )


# -------------------------
# ADMIN - STUDENTS
# -------------------------

@app.route("/admin/students")
@admin_required
def admin_students():

    admin = User.query.get(
        session["user_id"]
    )

    students = User.query.filter_by(
        college_id=admin.college_id,
        role="student"
    ).order_by(
        User.full_name.asc()
    ).all()

    return render_template(
        "admin/students.html",
        students=students,
        college=admin.college
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    # =========================================
    # CHECK LOGIN
    # =========================================

    if "user_id" not in session:

        flash(
            "Please login to access your dashboard.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    # =========================================
    # GET USER
    # =========================================

    user = User.query.get(
        session["user_id"]
    )

    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )

    # =========================================
    # PROJECT COUNT
    # =========================================

    project_count = Project.query.filter_by(
        user_id=user.id
    ).count()

    # =========================================
    # CODEFORCES ACCOUNT
    # =========================================

    codeforces_account = PlatformAccount.query.filter_by(
        user_id=user.id,
        platform="Codeforces"
    ).first()

    codeforces_stats = None

    if codeforces_account:

        codeforces_stats = PlatformStats.query.filter_by(
            platform_account_id=codeforces_account.id
        ).first()

    # =========================================
    # CONNECTED ACCOUNTS
    # =========================================

    connected_accounts = PlatformAccount.query.filter_by(
        user_id=user.id
    ).all()

    return render_template(
        "dashboard/dashboard.html",
        user=user,
        project_count=project_count,
        codeforces_stats=codeforces_stats,
        connected_accounts=connected_accounts
    )


# =========================================================
# PROJECTS
# =========================================================

# -------------------------
# ADD PROJECT
# -------------------------

@app.route("/projects/add", methods=["GET", "POST"])
def add_project():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        github_url = request.form.get("github_url")
        live_url = request.form.get("live_url")
        tech_stack = request.form.get("tech_stack")
        status = request.form.get("status")

        new_project = Project(
            user_id=session["user_id"],
            title=title,
            description=description,
            github_url=github_url,
            live_url=live_url,
            tech_stack=tech_stack,
            status=status
        )

        db.session.add(new_project)
        db.session.commit()

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "projects/add_project.html"
    )


# =========================================================
# CODING PLATFORMS
# =========================================================

# -------------------------
# PLATFORM ACCOUNTS
# -------------------------

@app.route("/platforms")
def platforms():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    accounts = PlatformAccount.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "platforms/accounts.html",
        accounts=accounts
    )


# -------------------------
# CONNECT PLATFORM
# -------------------------

@app.route("/platforms/connect", methods=["GET", "POST"])
def connect_platform():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        platform = request.form.get("platform")
        username = request.form.get("username")

        if not platform or not username:

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for("connect_platform")
            )

        profile_url = None

        if platform == "LeetCode":

            profile_url = (
                f"https://leetcode.com/u/{username}/"
            )

        elif platform == "Codeforces":

            profile_url = (
                f"https://codeforces.com/profile/{username}"
            )

        # =========================================
        # CHECK EXISTING ACCOUNT
        # =========================================

        existing_account = PlatformAccount.query.filter_by(
            user_id=session["user_id"],
            platform=platform
        ).first()

        if existing_account:

            existing_account.username = username
            existing_account.profile_url = profile_url
            existing_account.verified = False

        else:

            new_account = PlatformAccount(
                user_id=session["user_id"],
                platform=platform,
                username=username,
                profile_url=profile_url
            )

            db.session.add(new_account)

        db.session.commit()

        flash(
            f"{platform} account connected successfully.",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "platforms/connect.html"
    )


# -------------------------
# VERIFY PLATFORM
# -------------------------

@app.route("/platforms/verify/<int:account_id>")
def verify_platform(account_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    account = PlatformAccount.query.filter_by(
        id=account_id,
        user_id=session["user_id"]
    ).first()

    if not account:

        flash(
            "Platform account not found.",
            "error"
        )

        return redirect(
            url_for("platforms")
        )

    verification_code = (
        generate_verification_code()
    )

    expiry = (
        get_verification_expiry()
    )

    account.verification_code = verification_code
    account.verification_expires_at = expiry
    account.verification_attempts = 0
    account.verified = False

    db.session.commit()

    return render_template(
        "platforms/verify.html",
        account=account
    )


# -------------------------
# SYNC PLATFORM
# -------------------------

@app.route("/platforms/sync/<int:account_id>")
def sync_platform(account_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    account = PlatformAccount.query.filter_by(
        id=account_id,
        user_id=session["user_id"]
    ).first()

    if not account:

        flash(
            "Platform account not found.",
            "error"
        )

        return redirect(
            url_for("platforms")
        )

    if account.platform == "Codeforces":

        try:

            sync_codeforces_account(
                account
            )

            flash(
                "Codeforces stats synced successfully.",
                "success"
            )

        except Exception as e:

            print(
                "Codeforces sync error:",
                e
            )

            flash(
                "Unable to sync Codeforces stats. Please try again.",
                "error"
            )

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("dashboard")
    )


# =========================================================
# CODEFORCES OAUTH
# =========================================================

# -------------------------
# AUTHORIZE
# -------------------------

@app.route(
    "/platforms/codeforces/authorize/<int:account_id>"
)
def codeforces_authorize(account_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    account = PlatformAccount.query.filter_by(
        id=account_id,
        user_id=session["user_id"],
        platform="Codeforces"
    ).first()

    if not account:

        flash(
            "Codeforces account not found.",
            "error"
        )

        return redirect(
            url_for("platforms")
        )

    redirect_uri = url_for(
        "codeforces_callback",
        _external=True
    )

    return oauth.codeforces.authorize_redirect(
        redirect_uri
    )


# -------------------------
# CALLBACK
# -------------------------

@app.route("/platforms/codeforces/callback")
def codeforces_callback():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    token = (
        oauth.codeforces.authorize_access_token()
    )

    user_info = token.get(
        "userinfo"
    )

    print(
        "Codeforces User Info:",
        user_info
    )

    return redirect(
        url_for("platforms")
    )


# =========================================================
# ONBOARDING
# =========================================================

# -------------------------
# WELCOME
# -------------------------

@app.route("/welcome")
def welcome():

    return render_template(
        "onboarding/welcome.html"
    )


# -------------------------
# BASIC INFORMATION
# -------------------------

@app.route("/basic-info")
def basic_info():

    return render_template(
        "onboarding/basic-info.html"
    )


# -------------------------
# SKILLS
# -------------------------

@app.route("/skills")
def skills():

    return render_template(
        "onboarding/skills.html"
    )


# -------------------------
# CONNECT
# -------------------------

@app.route("/connect")
def connect():

    return render_template(
        "onboarding/connect.html"
    )


# -------------------------
# COMPLETE
# -------------------------

@app.route("/complete")
def complete():

    return render_template(
        "onboarding/complete.html"
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )