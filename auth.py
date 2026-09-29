import hashlib
import hmac
import secrets

from database import (
    create_user,
    get_user_by_email,
    count_users
)


def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_bytes(32)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        150000
    )

    return (
        password_hash.hex(),
        salt.hex()
    )


def verify_password(password, stored_hash, stored_salt):

    salt = bytes.fromhex(stored_salt)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        150000
    )

    return hmac.compare_digest(
        password_hash.hex(),
        stored_hash
    )


def validate_password(password):

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."

    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."

    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."

    return True, ""


def register_user(name, email, password):

    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Please enter your name."

    if "@" not in email:
        return False, "Please enter a valid email."

    valid, message = validate_password(password)

    if not valid:
        return False, message

    if get_user_by_email(email):
        return False, "An account with this email already exists."

    password_hash, salt = hash_password(password)

    user_id = create_user(
        name,
        email,
        password_hash,
        salt,
        "user"
    )

    if user_id is None:
        return False, "Unable to create account."

    return True, "Account created successfully."


def create_first_admin(name, email, password):

    if count_users() > 0:
        return False, "Admin setup is already completed."

    valid, message = validate_password(password)

    if not valid:
        return False, message

    password_hash, salt = hash_password(password)

    user_id = create_user(
        name,
        email,
        password_hash,
        salt,
        "admin"
    )

    if user_id is None:
        return False, "Unable to create admin."

    return True, "Admin account created successfully."


def login_user(email, password):

    email = email.strip().lower()

    user = get_user_by_email(email)

    if not user:
        return False, "Invalid email or password.", None

    if not user["is_active"]:
        return False, "This account has been disabled.", None

    valid = verify_password(
        password,
        user["password_hash"],
        user["salt"]
    )

    if not valid:
        return False, "Invalid email or password.", None

    return True, "Login successful.", user