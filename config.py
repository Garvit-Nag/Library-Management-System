import os
from typing import Final

class Config:
    SECRET_KEY: Final[str] = os.urandom(24)
    DATABASE_PATH: Final[str] = os.path.join(os.path.dirname(__file__), 'library.db')
    TOKEN_EXPIRATION: Final[int] = 3600  # 1 hour token expiration
    PAGE_SIZE: Final[int] = 10  # Default pagination size