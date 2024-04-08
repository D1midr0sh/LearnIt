from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    small_desc = StringField("Small description", validators=[DataRequired()])
    content = PageDownField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish")
