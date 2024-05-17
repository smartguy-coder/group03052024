from utils import validators


def test_is_valid_email():
    assert validators.is_valid_email("test_hillel_api_mailing@ukr.net")


def test_is_valid_email_1():
    assert validators.is_valid_email("test_hillel@ukr.net")


def test_is_valid_email_incorrect_email():
    assert not validators.is_valid_email("test_hillel_api_mailing@")


def test_is_valid_email_incorrect_email_2():
    assert not validators.is_valid_email("test_hillel_api_mailing")


def test_is_valid_email_incorrect_email_3():
    assert not validators.is_valid_email("")


def test_is_string():
    actual_result = validators.is_string("gg")
    expected_result = True
    assert actual_result is expected_result


def test_is_string_2():
    actual_result = validators.is_string(5)
    expected_result = False
    assert actual_result is expected_result
