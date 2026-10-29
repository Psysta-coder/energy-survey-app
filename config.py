"""Local configuration for the fictional-data test application.

All paths are inside the project folder. Nothing here contacts the internet.
"""
import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DEFAULT_DATABASE = os.path.join(INSTANCE_DIR, "test_data.db")
SECRET_KEY_FILE = os.path.join(INSTANCE_DIR, "secret_key.txt")


def load_secret_key():
    """Return a secret key for signing session cookies.

    Uses the FLASK_SECRET_KEY environment variable if set. Otherwise creates a
    random key once and stores it in the instance folder on this computer.
    """
    env_key = os.environ.get("FLASK_SECRET_KEY")
    if env_key:
        return env_key
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    if os.path.exists(SECRET_KEY_FILE):
        with open(SECRET_KEY_FILE, "r", encoding="utf-8") as handle:
            stored = handle.read().strip()
        if stored:
            return stored
    new_key = secrets.token_hex(32)
    with open(SECRET_KEY_FILE, "w", encoding="utf-8") as handle:
        handle.write(new_key)
    return new_key
