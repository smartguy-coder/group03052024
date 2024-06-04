from utils import email_sender


def main():
    inner_html_body = email_sender.create_welcome_letter(
        {"name": "Alex", "hobbies": ["tennis", "soccer"], "has_car": True}
    )
    print(inner_html_body)
    email_sender.send_email(
        ["test_hillel_api_mailing@ukr.net", "dduckker@ukr.net"],
        mail_body=inner_html_body,
        mail_subject="mail_subject",
        # attachment='2024-05-21_199-25.png',
    )


if __name__ == "__main__":
    main()
