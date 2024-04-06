import sqlalchemy

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