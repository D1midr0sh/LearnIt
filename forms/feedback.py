from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")
