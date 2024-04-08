from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_mail import Mail
from flask_pagedown import PageDown

import os

from data.db_session import create_session, global_init
from data.articles import Article
from data.users import User
from forms.article import ArticleForm
from forms.feedback import FeedbackForm
from forms.login import LoginForm
from forms.signup import SignUpForm
from email_send import send_email


load_dotenv()


app = Flask(__name__)
login_manager = LoginManager(app)
pagedown = PageDown(app)
app.config['MAIL_SERVER'] = 'smtp.timeweb.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
ADMIN_EMAIL = os.environ.get("MAIL_ADMINS").split(",")
mail = Mail(app)
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


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = FeedbackForm()
    if request.method == "GET":
        return render_template("contacts.html", form=form)
    if form.validate_on_submit():
        send_email(
            "Thank you for your feedback",
            sender=ADMIN_EMAIL[0],
            recipients=[form.email.data],
            text_body=render_template(
                "mail/feedback_reply.txt",
                name=form.name.data,
                message=form.message.data
            ),
            html_body=render_template(
                "mail/feedback_reply.html",
                name=form.name.data,
                message=form.message.data
            ),
            app=app
        )
        message = "Your feedback has been sent"
        return render_template("contacts.html", form=form, message=message)
    return render_template("contacts.html", form=form)


@app.route("/articles")
def articles():
    with create_session() as db_sess:
        articles = db_sess.query(Article).all()
        return render_template("articles/articles.html", articles=articles)


@app.route("/article/<int:id>", methods=["GET", "POST"])
def article(id: int):
    with create_session() as db_sess:
        article = db_sess.query(Article).get(id)
        return render_template("articles/article.html", article=article)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = ArticleForm()
    if form.validate_on_submit():
        with create_session() as db_sess:
            article = Article(
                title=form.title.data,
                small_desc=form.small_desc.data,
                content=form.content.data,
                user=current_user
            )
            db_sess.add(article)
            db_sess.commit()
            return redirect(f"/article/{article.id}")
    return render_template("articles/newarticle.html", form=form)


@app.route("/profile/<int:id>")
@login_required
def profile(id: int):
    with create_session() as db_sess:
        user = db_sess.query(User).get(id)
        return render_template("profile.html", user=user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template(
                "auth/signup.html",
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
            small_desc=form.small_desc.data
        )
        with create_session() as session:
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
        send_email(
            "Thank you for registering",
            sender=ADMIN_EMAIL[0],
            recipients=[form.email.data],
            text_body=render_template("mail/new_user.txt",
                                      first_name=form.first_name.data),
            html_body=render_template("mail/new_user.html",
                                      first_name=form.first_name.data),
            app=app
        )
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
