from flask import Flask, render_template, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from models import db, User, Application
from config import Config
import json, os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile'}
)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/login")
def login():
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
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = User.query.filter_by(email=session["user"]).first()

    if user.role == "officer":
        applications = Application.query.all()
        return render_template("officer.html", applications=applications)

    return render_template("citizen.html")

@app.route("/apply/<scheme>")
def apply(scheme):
    if "user" not in session:
        return redirect("/")

    new_app = Application(
        user_email=session["user"],
        scheme_name=scheme
    )
    db.session.add(new_app)
    db.session.commit()

    return "Application Submitted!"

@app.route("/approve/<int:id>")
def approve(id):
    app_obj = Application.query.get(id)
    app_obj.status = "Approved"
    db.session.commit()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)