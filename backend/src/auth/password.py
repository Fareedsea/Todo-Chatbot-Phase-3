"""
Password hashing and verification using bcrypt.

SECURITY REQUIREMENTS:
- Passwords MUST be hashed before storage (never plaintext)
- Bcrypt provides automatic salt generation
- Verification uses constant-time comparison (prevents timing attacks)
- 12 rounds (default) balances security and performance
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password: Plaintext password string

    Returns:
        Bcrypt-hashed password string (includes salt)

    Security:
        - Uses 12 rounds (bcrypt default)
        - Salt is automatically generated and embedded in hash
        - Result format: $2b$12$<salt><hash>
        - Never log or expose the plaintext password

    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> len(hashed) > 50  # Hash is ~60 characters
        True
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Bcrypt hash from database

    Returns:
        True if password matches, False otherwise

    Security:
        - Uses constant-time comparison (prevents timing attacks)
        - Extracts salt from hash automatically
        - Safe against rainbow table attacks (unique salt per password)

    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> verify_password("SecurePass123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False
