from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField


class ProfileEditForm(FlaskForm):
    first_name = StringField("First name")
    last_name = StringField("Last name")
    small_desc = StringField("Small description")
    submit = SubmitField("Submit")
    avatar = FileField("Your avatar")
