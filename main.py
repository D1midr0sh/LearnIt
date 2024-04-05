from dotenv import load_dotenv
from flask import Flask, render_template

import os


load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret")
app.config["DEBUG"] = os.environ.get("DEBUG", "No").lower() in ["true", "yes", "1"]


def main():
    app.run()


@app.route("/")
def base():
    return render_template("index.html")


@app.route("/articles")
def articles():
    return render_template("articles.html")


if __name__ == "__main__":
    main()
