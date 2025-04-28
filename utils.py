import random
import string
import redis
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Function to generate a 6-digit verification token
def generate_verification_token(length=6):
    return ''.join(random.choices(string.digits, k=length))

# Function to save token temporarily in Redis
def store_token(email, token, expiration_seconds=300):
    redis_client.setex(f"verify:{email}", expiration_seconds, token)

# Function to retrieve token from Redis
def retrieve_token(email):
    return redis_client.get(f"verify:{email}")

# Function to send the verification email
def send_verification_email(receiver_email, token):
    sender_email = os.getenv("SENDER_EMAIL") 
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print(f"Mock sending email to {receiver_email}: Your code is {token}")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Verification Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Your verification code is: {token}"
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    # Connect to SMTP server (example with Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
