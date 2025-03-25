from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing(data: str):
    return context.hash(data)

def verify(password: str, hashed_password: str):
    return context.verify(password, hashed_password)
