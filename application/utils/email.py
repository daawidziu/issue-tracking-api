from flask import render_template, current_app
from flask_mail import Message

from application import mail


def send_confirmation(email: str, confirmation_url: str) -> None:
    """Send confirmation email using Gmail Smtp"""
    msg = Message(
        subject='Account Confirmation',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email],
        html=render_template('confirmation.html', confirmation_url=confirmation_url))
    mail.send(msg)
