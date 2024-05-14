def is_valid_email(email_candidate: str) -> bool:
    if email_candidate.count("@") > 1:
        return False

    email_parts = email_candidate.strip("@").split("@")
    if len(email_parts) == 2:
        return True
    return False
