from flask_mail import Mail, Message

from utilities import asyncron


@asyncron
def send_async_email(app, msg):
    with app.app_context():
        mail = Mail(app)
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, app):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)
