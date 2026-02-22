from flask import Flask, redirect, url_for, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import json

app = Flask(__name__)

# Fix HTTPS behind Railway proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(50), default="citizen")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150))
    scheme_name = db.Column(db.String(200))
    status = db.Column(db.String(50), default="Pending")

# Create tables
with app.app_context():
    db.create_all()

# ================= GOOGLE OAUTH =================
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# ================= ROUTES =================

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    resp = google.get("https://openidconnect.googleapis.com/v1/userinfo")
    user_info = resp.json()

    email = user_info.get("email")

    if not email:
        return "Error fetching email from Google"

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    session["user"] = email
    return redirect(url_for("dashboard"))


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    user = User.query.filter_by(email=session["user"]).first()

    # Load schemes safely
    basedir = os.path.abspath(os.path.dirname(__file__))
    schemes_path = os.path.join(basedir, "data", "schemes.json")

    schemes = []
    if os.path.exists(schemes_path):
        with open(schemes_path, "r") as f:
            schemes = json.load(f)

    if user.role == "officer":
        applications = Application.query.all()
        return render_template("officer.html", applications=applications)

    return render_template("dashboard.html", schemes=schemes)


# ================= ELIGIBILITY CHECK =================
@app.route("/check", methods=["POST"])
def check_eligibility():
    if "user" not in session:
        return redirect(url_for("home"))

    income = int(request.form.get("income", 0))
    occupation = request.form.get("occupation", "").strip()
    gender = request.form.get("gender")
    land = request.form.get("land")
    district = request.form.get("district", "").strip()

    basedir = os.path.abspath(os.path.dirname(__file__))
    schemes_path = os.path.join(basedir, "data", "schemes.json")

    with open(schemes_path, "r") as f:
        all_schemes = json.load(f)

    eligible = []

    for scheme in all_schemes:

        # Income check
        if income > scheme.get("income_limit", 999999):
            continue

        # Occupation check
        scheme_occ = scheme.get("occupation")
        if scheme_occ and occupation:
            if isinstance(scheme_occ, list):
                if occupation not in scheme_occ:
                    continue
            elif scheme_occ != "Any" and scheme_occ != occupation:
                continue

        # Gender check
        if scheme.get("gender_required"):
            if scheme["gender_required"] != gender:
                continue

        # Land check
        if land:
            land_bool = land == "true"
            if scheme.get("land_required", False) != land_bool:
                continue

        # District check
        scheme_district = scheme.get("districts")
        if scheme_district != "All" and district:
            if isinstance(scheme_district, list):
                if district not in scheme_district:
                    continue
            elif scheme_district != district:
                continue

        eligible.append(scheme)

    return render_template("dashboard.html", schemes=eligible)


# ================= APPLY =================
@app.route("/apply/<scheme>")
def apply(scheme):
    if "user" not in session:
        return redirect(url_for("home"))

    new_application = Application(
        user_email=session["user"],
        scheme_name=scheme
    )
    db.session.add(new_application)
    db.session.commit()

    return redirect(url_for("dashboard"))


# ================= APPROVE =================
@app.route("/approve/<int:id>")
def approve(id):
    application = Application.query.get(id)
    if application:
        application.status = "Approved"
        db.session.commit()
    return redirect(url_for("dashboard"))


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)