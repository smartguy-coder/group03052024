import os

from dotenv import load_dotenv

load_dotenv()


TOKEN_API = os.getenv("TOKEN_API")
USER = os.getenv("USER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
IMAP_SERVER = os.getenv("IMAP_SERVER")
