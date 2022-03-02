from flask import render_template, current_app
import boto3


ses = boto3.client(
    "ses",
    region_name=current_app.config["SES_REGION"],
    aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"]
)


def send_confirmation(email: str, confirmation_url: str) -> None:
    """Send confirmation email using AWS SES"""
    ses.send_email(
        Source=current_app.config["SES_EMAIL_SOURCE"],
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Confirm Your Account!"},
            "Body": {
                "Html": {"Data": render_template("confirmation.html", confirmation_url=confirmation_url)}
            }
        }
    )
