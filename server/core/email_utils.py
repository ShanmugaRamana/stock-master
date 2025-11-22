import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Change this to your production URL later. For now, localhost.
BASE_URL = "http://127.0.0.1:8000"

def send_verification_email(to_email: str, token: str):
    subject = "Verify your Stock Master Account"
    verify_link = f"{BASE_URL}/verify?token={token}"
    
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
            <h2 style="color: #000;">Welcome to Stock Master!</h2>
            <p>Please verify your account to enable login access.</p>
            <br>
            <div style="text-align: center;">
                <a href="{verify_link}" style="background-color: #000000; color: #ffffff; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 16px;">Verify Account</a>
            </div>
            <br>
            <p style="font-size: 12px; color: #999;">If you did not create this account, please ignore this email.</p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        print("Verification email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")