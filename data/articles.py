import bleach
import sqlalchemy
from markdown import markdown
import sqlalchemy.event

from .db_session import SqlAlchemyBase


class Article(SqlAlchemyBase):
    __tablename__ = "articles"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    small_desc = sqlalchemy.Column(sqlalchemy.VARCHAR(70), nullable=True)
    content = sqlalchemy.Column(sqlalchemy.Text)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship("User")

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "pre",
            "strong",
            "ul",
            "h1",
            "h2",
            "h3",
            "p",
        ]
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format="html"), tags=allowed_tags, strip=True
            )
        )


sqlalchemy.event.listen(Article.content, "set", Article.on_changed_body)
