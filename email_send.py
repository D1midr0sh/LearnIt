from flask_mail import Mail, Message

from utilities import asyncron


@asyncron
def send_async_email(app, msg):
    mail = Mail(app)
    mail.send(msg)


def send_email(subject, sender, recipicents, text_body, html_body, app):
    msg = Message(subject, sender=sender, recipients=recipicents)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)
