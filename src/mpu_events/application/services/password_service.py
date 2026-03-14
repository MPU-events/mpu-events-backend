import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    @staticmethod
    def _pre_hash(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def hash(password: str) -> str:
        pre_hashed = PasswordService._pre_hash(password)
        return pwd_context.hash(pre_hashed)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        pre_hashed = PasswordService._pre_hash(plain_password)
        return pwd_context.verify(pre_hashed, hashed_password)