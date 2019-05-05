from passlib.hash import bcrypt


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)


def get_password_hash(plain_password: str) -> str:
    """
    Get a hash for user's password
    :param plain_password: password as text
    :return: hashed password
    """
    return bcrypt.hash(plain_password)