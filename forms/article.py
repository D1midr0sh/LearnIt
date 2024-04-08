from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    small_desc = StringField(
        "Small description", validators=[DataRequired(), Length(min=0, max=70)]
    )
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish")
