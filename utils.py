import os
import random
import string
import redis
from redis import exceptions as redis_exceptions
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    # verify connection
    redis_client.ping()
except redis_exceptions.ConnectionError:
    print(f"[WARN] Could not connect to Redis at {REDIS_URL}. Using in-memory store.")
    class _DummyRedis:
        def __init__(self):
            self._store = {}
        def setex(self, key, ttl, value):
            self._store[key] = value
        def get(self, key):
            return self._store.get(key)
        def delete(self, key):
            self._store.pop(key, None)
    redis_client = _DummyRedis()


def generate_verification_token(length=6):
    """Generate a random numeric verification token."""
    return ''.join(random.choices(string.digits, k=length))


def store_token(email, token, expiration_seconds=300):
    """Store token in Redis with an expiration."""
    try:
        redis_client.setex(f"verify:{email}", expiration_seconds, token)
    except Exception as e:
        # Log or handle as needed
        print(f"[ERROR] Failed to store token for {email}: {e}")
        raise


def retrieve_token(email):
    """Retrieve token from Redis."""
    try:
        return redis_client.get(f"verify:{email}")
    except Exception as e:
        print(f"[ERROR] Failed to retrieve token for {email}: {e}")
        return None


def send_verification_email(receiver_email, token):
    """Send the verification email, or mock if SMTP credentials are missing."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 465))

    if not sender_email or not sender_password:
        print(f"[MOCK EMAIL] To: {receiver_email}\nYour verification code is: {token}")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Verification Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Your verification code is: {token}"
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"[ERROR] Failed to send email to {receiver_email}: {e}")
        raise
