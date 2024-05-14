def is_valid_email(email_candidate: str) -> bool:
    return False
    print(f'{email_candidate.count("@")=}')
    if email_candidate.count("@") > 1:
        return False

    email_parts = email_candidate.strip("@").split("@")
    print(f"{email_parts=}")
    if len(email_parts) == 2:
        return True
    return False
