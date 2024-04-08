from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    small_desc = StringField("Small description")
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Submit")
