from dotenv import load_dotenv
from flask import Flask

import os
import logging


logging.basicConfig(level=logging.DEBUG)
load_dotenv()


app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.timeweb.ru"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret")
app.config["DEBUG"] = os.environ.get("DEBUG", "No").lower() in ["true", "yes", "1"]

ADMIN_EMAIL = os.environ.get("MAIL_ADMINS").split(",")

app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = "img/user_avatars/"
app.config["SAVE_PATH"] = "static/img/user_avatars/"
