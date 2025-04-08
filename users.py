from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_user_db = {
    "reddappa": {
        "username": "reddappa",
        "hashed_password": pwd_context.hash("ajsdnksjandlkjans"),
    }
}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str):
    user = fake_user_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
