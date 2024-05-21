import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_email(
    recipients: list[str],
    mail_body: str,
    mail_subject: str,
    attachment: str = None,
) -> None:
    TOKEN_API = config.TOKEN_API
    USER = config.USER
    SMTP_SERVER = config.SMTP_SERVER

    msg = MIMEMultipart("alternative")
    msg["Subject"] = mail_subject
    msg["From"] = f"{USER} sent this email"
    msg["To"] = ", ".join(recipients)
    msg["Reply-To"] = USER
    msg["Return-Path"] = USER
    msg["X-Mailer"] = "decorator"

    if attachment:
        is_file_exists = os.path.exists(attachment)
        if not is_file_exists:
            print(f'file {attachment} does`n exist')
        else:
            basename = os.path.basename(attachment)
            filesize = os.path.getsize(attachment)
            file = MIMEBase('application', f'octet-stream; name={basename}')
            file.set_payload(open(attachment, 'rb').read())
            file.add_header('Content-Description', attachment)
            file.add_header('Content-Description', f'attachment; filename={attachment}; size={filesize}')
            encoders.encode_base64(file)
            msg.attach(file)

    text_to_send = MIMEText(mail_body, "plain")
    msg.attach(text_to_send)

    mail = smtplib.SMTP_SSL(SMTP_SERVER)
    mail.login(USER, TOKEN_API)
    mail.sendmail(USER, recipients, msg.as_string())
    mail.quit()
