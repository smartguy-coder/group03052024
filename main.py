from utils import email_sender


def main():
    email_sender.send_email(
        recipients=["test_hillel_api_mailing@ukr.net", "dduckker@ukr.net"],
        mail_body="fffffff",
        mail_subject="gggggg",
        attachment='2024-05-21_19-25.png',
    )


if __name__ == "__main__":
    main()
