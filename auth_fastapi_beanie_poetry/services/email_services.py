import aiosmtplib
from email.mime.text import MIMEText
from auth_fastapi_beanie_poetry.core.config import core_settings
from jinja2 import Environment, FileSystemLoader
import os

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('auth_fastapi_beanie_poetry/templates'))

async def send_password_reset(email: str, token: str):
    """
    Send a password reset email asynchronously using aiosmtplib.
    """
    reset_link = f"{core_settings.FULL_URL}/reset-password?token={token}"
    
    # Load the HTML template
    template = env.get_template('reset_password.html')
    # Create user object with necessary details
    user = {
        "email": email,
        "reset_link": reset_link,
        "username": email.split('@')[0],  # Extract username from email
        "contact_support": "www.ricospice.store/contact",
        "domain": "www.ricospice.store",
        "href_domain": "https://www.ricospice.store",
    }
    context = {
      "reset_link": user["reset_link"],
      "username": user["username"],
      "contact_support": user["contact_support"],
      "domain": user["domain"],
      "href_domain": user["href_domain"],
    }
    # Render the template with context
    html_body = template.render(context)
    
    subject = "Password Reset Request"
    # Create email message
    msg = MIMEText(html_body, 'html')
    msg["Subject"] = subject
    msg["From"] = core_settings.MAIL_FROM
    msg["To"] = email

    try:
        print(f"mail_port: {core_settings.MAIL_PORT}")
        print(f"mail_server: {core_settings.MAIL_SERVER}")
        print(f"mail_ssl_tls: {core_settings.MAIL_SSL_TLS}")
        await aiosmtplib.send(
            msg,
            hostname=core_settings.MAIL_SERVER,
            port=core_settings.MAIL_PORT,
            start_tls=core_settings.MAIL_SSL_TLS,
            # Uncomment and update if authentication is needed:
            username=core_settings.MAIL_USERNAME,
            password=core_settings.MAIL_PASSWORD,
        )
        print(f"Password reset email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        # Handle error appropriately (e.g., log error)