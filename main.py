from utils import email_sender

print("from main", __name__)


def main():
    email_sender.send_email(recipients=["test_hillel_api_mailing@ukr.net"], mail_body="fffffff", mail_subject="gggggg")


if __name__ == "__main__":
    main()
