from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import generate_password_hash, check_password_hash
from app.services.image_service import resize_image
from app.extensions import db
from app.models.user import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required.")
            return render_template("signup.html")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.")
            return render_template("signup.html")

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.")
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Invalid email or password.")
            return render_template("login.html")

        if not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.")
            return render_template("login.html")

        session["user_id"] = user.id
        session["username"] = user.username

        flash("Login successful.")
        return redirect(url_for("auth.dashboard"))

    return render_template("login.html")


@auth_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("auth.login"))

    return render_template(
        "dashboard.html",
        username=session.get("username")
    )

@auth_bp.route("/resize", methods=["POST"])
def resize():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("auth.login"))

    if "image" not in request.files:
        flash("No image selected.")
        return redirect(url_for("auth.dashboard"))

    image = request.files["image"]

    if image.filename == "":
        flash("No image selected.")
        return redirect(url_for("auth.dashboard"))

    try:
        result = resize_image(
            image,
            session["username"]
        )

        flash("Image resized successfully.")

        return render_template(
            "dashboard.html",
            username=session.get("username"),
            original_path=result["original"],
            resized_path=result["resized"]
        )

    except ValueError as error:
        flash(str(error))
        return redirect(url_for("auth.dashboard"))

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
