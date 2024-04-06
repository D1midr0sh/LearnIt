from dotenv import load_dotenv
from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user

import os

from data.db_session import create_session, global_init
from data.users import User
from forms.login import LoginForm
from forms.signup import SignUpForm


load_dotenv()


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret")
app.config["DEBUG"] = os.environ.get("DEBUG", "No").lower() in ["true", "yes", "1"]


@login_manager.user_loader
def load_user(user_id):
    with create_session() as db_sess:
        return db_sess.query(User).get(user_id)


def main():
    global_init("db/database.db")
    app.run()


@app.route("/")
def base():
    return render_template("index.html")


@app.route("/articles")
def articles():
    return render_template("articles.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template(
                "signup.html",
                form=form,
                message="Passwords do not match"
            )
        with create_session() as session:
            if session.query(User).where(User.email == form.email.data).first():
                return render_template(
                    "auth/signup.html",
                    form=form,
                    message="User with this email already exists"
                )
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
        )
        with create_session() as session:
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
        return redirect("/")
    return render_template("auth/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with create_session() as session:
            user = session.query(User).where(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect("/")
            return render_template(
                "auth/login.html",
                form=form,
                message="Wrong email or password"
            )
    return render_template("auth/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    main()
