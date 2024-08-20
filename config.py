import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = False

TOKEN_API = os.getenv("TOKEN_API")
EMAIL_USER = os.getenv("EMAIL_USER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
IMAP_SERVER = os.getenv("IMAP_SERVER")
DB_PATH = os.getenv("DB_PATH") or ""
STRIPE_KEY = os.getenv("STRIPE_KEY") or ""
SENTRY_KEY = os.getenv("SENTRY_KEY") or ""

JWT_KEY = os.getenv("JWT_KEY")
