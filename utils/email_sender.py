import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(
    recipients: list[str],
    mail_body: str,
    mail_subject: str,
    attachments: str = None,
)-> None:

    TOKEN_API = config.TOKEN_API
    USER = config.USER
    SMTP_SERVER = config.SMTP_SERVER

    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_subject
    msg['From'] = f'{USER} sent this email'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = USER
    msg['Return-Path'] = USER
    msg['X-Mailer'] = 'decorator'

    text_to_send = MIMEText(mail_body, 'plain')
    msg.attach(text_to_send)




