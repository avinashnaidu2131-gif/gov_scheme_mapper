from flask import Flask, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)

# 🔥 IMPORTANT: Fix HTTPS behind Railway proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# ================= SECRET KEY =================
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# ================= DATABASE CONFIG (SQLite) =================
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

# Create DB tables
with app.app_context():
    db.create_all()

# ================= GOOGLE OAUTH =================
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)
# ================= ROUTES =================

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login")
def login():
    # 🔥 This must match Google Console redirect URI
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)

    email = user_info["email"]

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, role="citizen")
        db.session.add(user)
        db.session.commit()

    session["user"] = email
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    user = User.query.filter_by(email=session["user"]).first()

    if user.role == "officer":
        applications = Application.query.all()
        return render_template("officer.html", applications=applications)

    return render_template("citizen.html")


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

    return "Application Submitted Successfully!"


@app.route("/approve/<int:id>")
def approve(id):
    application = Application.query.get(id)
    application.status = "Approved"
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)