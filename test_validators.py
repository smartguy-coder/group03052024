from utils import validators


def test_is_valid_email():
    assert validators.is_valid_email("test_hillel_api_mailing@ukr.net")


def test_is_valid_email_incorrect_email():
    assert not validators.is_valid_email("test_hillel_api_mailing@")
